#!/usr/bin/env python3
"""Probes de isolamento para runner GitHub Actions: sem OpenHands/LLM/segredos.

Executar somente em runner efêmero autorizado. Falha/indisponibilidade da
sandbox = falha do job (NO-GO), nunca skip ou fallback ao shell do host.
"""
from __future__ import annotations

import hashlib
import os
from pathlib import Path
import shutil
import signal
import socket
import subprocess
import sys
import tempfile
import time
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))
from canary_controls import ALLOWED, GateError, sandbox_argv, snapshot, supervise


class SandboxRunnerProbe(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="observatorio-sandbox-probe-")
        cls.addClassCleanup(cls.temp.cleanup)
        cls.base = Path(cls.temp.name).resolve()
        source = cls.base / "source"
        source.mkdir()
        for command, argv in ALLOWED.items():
            if len(argv) == 2:
                destination = source / argv[1]
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_text("CONTEUDO_PUBLICO_SINTETICO\n", encoding="utf-8")
        cls.host_marker = cls.base / "fora-do-snapshot.txt"
        cls.host_marker.write_text("MARCADOR_SINTETICO", encoding="utf-8")
        cls.root = snapshot(source, cls.base / "state")
        cls.approved = sorted(cls.root.rglob("*"))
        cls.file_hashes = {
            str(p.relative_to(cls.root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in cls.approved if p.is_file()
        }

    def run_protected(self, python_code=None, args=(), inherited_env=None):
        argv = sandbox_argv(self.root, "pwd")
        if python_code is not None:
            # Substituição SOMENTE no harness de prova, nunca no executor operacional.
            argv = argv[:-1] + ["/usr/bin/python3", "-I", "-c", python_code, *args]
        return subprocess.run(
            argv,
            env=inherited_env if inherited_env is not None else {},
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=15,
            check=False,
        )

    def assert_sandbox_passed(self, result, label):
        self.assertEqual(
            result.returncode, 0,
            msg=(
                label + " NO-GO: bwrap não executou a prova ou uma restrição falhou. "
                + "exit=" + str(result.returncode)
                + " stderr=" + result.stderr[:320].replace("\n", " ")
            ),
        )

    def test_01_bwrap_real_e_leitura_permitida(self):
        self.assertEqual(shutil.which("bwrap"), "/usr/bin/bwrap", "NO-GO: bwrap ausente")
        result = self.run_protected()
        self.assert_sandbox_passed(result, "startup")
        self.assertEqual(result.stdout.strip(), "/workspace")
        # Prova usando a mesma montagem/argv do executor real, sem shell.
        output = supervise(sandbox_argv(self.root, "cat AGENTS.md"), 10)
        self.assertEqual(output.strip(), "CONTEUDO_PUBLICO_SINTETICO")

    def test_02_snapshot_somente_leitura(self):
        code = (
            "from pathlib import Path\n"
            "p=Path('/workspace/AGENTS.md')\n"
            "assert p.read_text().strip() == 'CONTEUDO_PUBLICO_SINTETICO'\n"
            "for target in (p,Path('/workspace/novo.txt')):\n"
            "  try:\n"
            "    target.write_text('ALTERACAO_PROIBIDA')\n"
            "  except OSError:\n"
            "    pass\n"
            "  else:\n"
            "    raise AssertionError('escrita inesperadamente permitida')\n"
        )
        self.assert_sandbox_passed(self.run_protected(code), "read-only")
        for p in self.root.rglob("*"):
            if p.is_file():
                rel = str(p.relative_to(self.root))
                self.assertEqual(
                    hashlib.sha256(p.read_bytes()).hexdigest(),
                    self.file_hashes[rel],
                    "snapshot foi modificado",
                )
        self.assertFalse((self.root / "novo.txt").exists())

    def test_03_sem_acesso_ao_host_ou_ambiente(self):
        self.assertTrue(self.host_marker.is_file())
        code = (
            "import os,sys\n"
            "from pathlib import Path\n"
            "assert os.getenv('CANARY_PROBE_MARKER') is None\n"
            "assert not Path(sys.argv[1]).exists(), 'arquivo do host ficou visivel'\n"
            "assert not Path('/workspace/.git').exists()\n"
            "assert not Path('/home/runner/work').exists()\n"
            "assert os.getcwd() == '/workspace'\n"
        )
        result = self.run_protected(
            code, (str(self.host_marker),),
            inherited_env={"CANARY_PROBE_MARKER": "valor_sintetico"},
        )
        self.assert_sandbox_passed(result, "host/environment")

    def test_04_rede_host_local_inacessivel(self):
        # Sem internet: tenta somente um listener efêmero da própria VM.
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as listener:
            listener.bind(("127.0.0.1", 0))
            listener.listen(1)
            port = listener.getsockname()[1]
            code = (
                "import socket,sys\n"
                "s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)\n"
                "s.settimeout(0.6)\n"
                "try:\n"
                "  rc=s.connect_ex(('127.0.0.1',int(sys.argv[1])))\n"
                "  assert rc!=0, 'rede do host alcancavel'\n"
                "except OSError:\n"
                "  pass\n"
                "finally:\n"
                "  s.close()\n"
            )
            self.assert_sandbox_passed(
                self.run_protected(code, (str(port),)), "network",
            )

    def test_05_sem_fallback_para_comando_nao_autorizado(self):
        for command in ("cat /etc/passwd", "env", "cat ../segredo", "curl x"):
            with self.subTest(command=command), self.assertRaises(GateError):
                sandbox_argv(self.root, command)

    def test_06_supervisor_encerra_grupo_e_descendente(self):
        # Processo sintético sem LLM; valida killpg no supervisor do código real.
        pid_file = self.base / "descendente.pid"
        code = (
            "import subprocess,sys,time\n"
            "child=subprocess.Popen(['/bin/sleep','30'])\n"
            "with open(sys.argv[1],'w') as f:\n"
            "  f.write(str(child.pid)); f.flush()\n"
            "time.sleep(30)\n"
        )
        with self.assertRaisesRegex(GateError, "worker_interrupted_or_timed_out"):
            supervise([sys.executable, "-c", code, str(pid_file)], 1.5)
        self.assertTrue(pid_file.is_file(), "processo sintético não iniciou")
        pid = int(pid_file.read_text(encoding="utf-8"))
        # Zumbi reaproveita PID até ser coletado, mas não executa.
        running = True
        for _ in range(20):
            try:
                state = Path("/proc") / str(pid) / "stat"
                if not state.exists():
                    running = False
                    break
                running = state.read_text().split(") ", 1)[1][0] != "Z"
            except (FileNotFoundError, ProcessLookupError):
                running = False
                break
            if not running:
                break
            time.sleep(0.1)
        self.assertFalse(running, "descendente permaneceu executando após timeout")


if __name__ == "__main__":
    unittest.main(verbosity=2)
