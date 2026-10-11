"""Fail-closed controls for a future canary. No OpenHands/LLM execution here."""
from __future__ import annotations
import math
import os
from pathlib import Path
import signal
import subprocess
import threading
import time

ALLOWED = {'pwd': ['/usr/bin/pwd'], **{
    'cat ' + path: ['/usr/bin/cat', path]
    for path in ('docs/PROJECT_SOURCE.md', 'AGENTS.md', 'team/README.md', 'team/catalog.json')
}}

class GateError(RuntimeError):
    """A gate prevented continuation; messages contain no operational payloads."""

class Guard:
    def __init__(self, max_calls=6, seconds=120., budget=.10, clock=time.monotonic):
        if type(max_calls) is not int or max_calls < 1:
            raise ValueError('invalid_call_limit')
        if any(type(x) not in (int,float) or not math.isfinite(x) or x <= 0 for x in (seconds,budget)):
            raise ValueError('invalid_limit')
        self.max_calls=max_calls; self.deadline=clock()+seconds; self.budget=budget; self.clock=clock
        self.calls=0; self.cost=0.; self.input_tokens=0; self.output_tokens=0
        self.cancelled=False; self.delegations=0; self.lock=threading.Lock()

    def claim_delegation(self, subagent_type):
        with self.lock:
            if self.cancelled or subagent_type!='code-explorer' or self.delegations!=0:
                self.cancelled=True
                raise GateError('delegation_not_allowed')
            self.delegations=1

    def cancel(self):
        with self.lock: self.cancelled=True

    def reserve(self):
        with self.lock:
            if self.cancelled or self.clock() >= self.deadline or self.calls >= self.max_calls or self.cost >= self.budget:
                self.cancelled=True
                raise GateError('global_limit')
            self.calls+=1

    def record(self, cost, input_tokens, output_tokens):
        with self.lock:
            if (type(cost) not in (float,int) or not math.isfinite(cost) or cost <= 0
                or any(type(x) is not int or x < 0 for x in (input_tokens,output_tokens))):
                self.cancelled=True
                raise GateError('usage_not_verifiable')
            self.cost+=cost; self.input_tokens+=input_tokens; self.output_tokens+=output_tokens
            if self.cost >= self.budget or self.clock() >= self.deadline:
                self.cancelled=True


def confirm(task_id, pending, approval=None):
    """Only an explicit True for every exact allowlisted action grants approval."""
    if approval is None or not pending:
        return False
    try:
        for event in pending:
            action=event.action
            if (getattr(action,'is_input',True) is not False or
                action.command not in ALLOWED or approval(task_id,action.command) is not True):
                return False
        return True
    except Exception:
        return False


def snapshot(source: Path, state: Path) -> Path:
    """Copy only reviewed public files; never mount a repository's .git or secrets."""
    source=source.absolute(); state=state.absolute()
    if source.resolve()!=source or state.resolve()!=state or source==state or source in state.parents:
        raise GateError('unsafe_snapshot_location')
    files={argv[1] for argv in ALLOWED.values() if len(argv)==2}
    contents={}
    for relative in files:
        path=source/relative
        if path.resolve()!=path or not path.is_file():
            raise GateError('unsafe_snapshot_file')
        contents[relative]=path.read_bytes()
    try:
        state.mkdir(mode=0o700,parents=True,exist_ok=False)
    except FileExistsError as error:
        raise GateError('state_must_be_fresh') from error
    root=state/'snapshot'; root.mkdir(mode=0o700)
    for relative, data in contents.items():
        target=root/relative; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
    return root


def sandbox_argv(root: Path, command: str) -> list[str]:
    if command not in ALLOWED:
        raise GateError('command_not_allowed')
    return ['/usr/bin/bwrap','--unshare-all','--die-with-parent','--new-session',
            '--clearenv','--cap-drop','ALL','--ro-bind','/usr','/usr',
            '--symlink','usr/bin','/bin','--symlink','usr/lib','/lib',
            '--symlink','usr/lib64','/lib64','--proc','/proc','--dev','/dev',
            '--tmpfs','/tmp','--dir','/home','--dir','/home/canary',
            '--setenv','HOME','/home/canary','--setenv','PATH','/usr/bin',
            '--ro-bind',str(root.absolute()),'/workspace','--chdir','/workspace',
            '--',*ALLOWED[command]]


def supervise(argv, seconds, popen=None):
    """Hard wall-clock kill for an isolated worker; never retry or inherit env/FDs."""
    if type(seconds) not in (int,float) or not math.isfinite(seconds) or seconds<=0:
        raise ValueError('invalid_timeout')
    proc=(popen or subprocess.Popen)(argv,env={},close_fds=True,start_new_session=True,
                                    stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE,text=True)
    try:
        stdout, _stderr=proc.communicate(timeout=seconds)
    except BaseException as error:
        try: os.killpg(proc.pid,signal.SIGKILL)
        except ProcessLookupError: pass
        proc.communicate()
        raise GateError('worker_interrupted_or_timed_out') from error
    if proc.returncode!=0:
        raise GateError('worker_failed_no_fallback')
    return stdout


def terminal_executor(root,guard,approval=None):
    """Callback usable by the official TerminalTool executor adapter, no shell."""
    from types import SimpleNamespace
    def execute(action):
        if guard.cancelled or guard.clock() >= guard.deadline:
            raise GateError('terminal_deadline')
        if not confirm('terminal',[SimpleNamespace(action=action)],approval):
            raise GateError('approval_missing_or_command_denied')
        try:
            return supervise(sandbox_argv(root,action.command),
                             min(30.,guard.deadline-guard.clock()))
        except BaseException:
            guard.cancel(); raise
    return execute


def quote(catalog,model,input_tokens,output_tokens):
    """Offline catalog estimate only, never a claim of account access/current prices."""
    try:
        rates=catalog[model]
        values=[rates['input_cost_per_token'],rates['output_cost_per_token']]
        if (any(type(v) not in (float,int) or not math.isfinite(v) or v<=0 for v in values)
            or any(type(v) is not int or v<0 for v in (input_tokens,output_tokens))):
            raise ValueError('invalid_rates_or_tokens')
        return input_tokens*values[0]+output_tokens*values[1]
    except (KeyError,TypeError,ValueError) as error:
        raise GateError('pricing_not_verified') from error
