"""Adapters for SDK 1.53.0. No CLI, credentials, registration or delegation calls."""
from contextlib import contextmanager
import importlib.metadata
import inspect
import math
from canary_controls import GateError, confirm


def sdk_bindings():
    if any(importlib.metadata.version(p)!='1.53.0' for p in ('openhands-sdk','openhands-tools')):
        raise GateError('sdk_version_mismatch')
    from openhands.sdk import Tool
    from openhands.tools import TaskToolSet, register_builtins_agents
    return Tool, TaskToolSet, register_builtins_agents


def task_spec(approval=None):
    """Return official tool spec with explicit fail-closed callback; does not execute."""
    Tool, TaskToolSet, _register=sdk_bindings()
    def callback(task_id,pending): return confirm(task_id,pending,approval)
    return Tool(name=TaskToolSet.name,params={'confirmation_handler':callback,
               'sub_agent_scope':{'tools':True,'mcp_servers':True}})


def _metrics(llm):
    try:
        metrics=llm.metrics
        usage=metrics.accumulated_token_usage
        values=(metrics.accumulated_cost,usage.prompt_tokens,usage.completion_tokens)
        if (type(values[0]) not in (int,float) or not math.isfinite(values[0]) or values[0]<0
            or any(type(v) is not int or v<0 for v in values[1:])):
            raise GateError('usage_invalid')
        return values
    except Exception as error:
        raise GateError('usage_missing') from error


@contextmanager
def guarded_llm(llm_class,guard):
    """Process-local API boundary guard shared by copies and all supported routes.

    Only for a dedicated future worker; must surround its entire lifespan.
    Never applied to an installed server. Wrapping routes may conservatively
    count nested fallback routes twice. Provider retries must stay zero.
    """
    originals={name:getattr(llm_class,name) for name in
               ('completion','acompletion','responses','aresponses')}
    def before(llm):
        if llm.num_retries != 0:
            guard.cancel(); raise GateError('retries_forbidden')
        guard.reserve()
        return _metrics(llm)
    def after(llm,start):
        finish=_metrics(llm)
        guard.record(*(a-b for a,b in zip(finish,start)))
    def wrap(fn):
        if inspect.iscoroutinefunction(fn):
            async def async_call(llm,*args,**kwargs):
                try:
                    start=before(llm); result=await fn(llm,*args,**kwargs); after(llm,start); return result
                except BaseException:
                    guard.cancel(); raise
            return async_call
        def call(llm,*args,**kwargs):
            try:
                start=before(llm);result=fn(llm,*args,**kwargs);after(llm,start);return result
            except BaseException:
                guard.cancel(); raise
        return call
    try:
        for name,fn in originals.items(): setattr(llm_class,name,wrap(fn))
        yield
    finally:
        for name,fn in originals.items(): setattr(llm_class,name,fn)


def terminal_tools(conv_state,root,guard,approval=None):
    """Use TerminalTool.create(executor=...) so builtin Explorer keeps its tool name.

    Returned tools are inert until an approved future worker registers the
    fixed instance using the official register_tool API in that process only.
    """
    from canary_controls import terminal_executor
    from openhands.sdk.tool import ToolExecutor
    from openhands.tools.terminal.definition import TerminalTool,TerminalObservation
    from openhands.tools.terminal.metadata import CmdOutputMetadata
    execute=terminal_executor(root,guard,approval)
    class RestrictedExecutor(ToolExecutor):
        def __call__(self,action,conversation=None):
            output=execute(action)
            return TerminalObservation.from_text(text=output,command=action.command,
                       exit_code=0,metadata=CmdOutputMetadata(exit_code=0,working_dir='/workspace'))
        def close(self): pass
    return TerminalTool.create(conv_state=conv_state,executor=RestrictedExecutor())


def explorer_action(guard):
    """Construct one official synthetic action, never dispatch it or resume a task."""
    from openhands.tools.task import TaskAction
    guard.claim_delegation('code-explorer')
    return TaskAction(subagent_type='code-explorer',resume=None,prompt=(
        'Read only the four public snapshot files using the approved exact cat commands. '
        'Summarize the repository identity and limits. Do not modify files, use network, '
        'read other paths, delegate, or start processes beyond the approved commands.'))
