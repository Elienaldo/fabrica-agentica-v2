#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes puros do aviso da V2 ao terminar a criação de seção. Sem rede, sem app, sem PowerShell real."""
from __future__ import annotations

import importlib
import importlib.util
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import notificacao_criacao_v2 as nc  # noqa: E402

URL = "https://api2.cursor.sh/automations/webhook/teste-falso-criacao"
KEY = "chave-falsa-criacao-ABC"
ENV = {nc.URL_ENV: URL, nc.KEY_ENV: KEY}
SEM_USER = lambda nome: ""  # noqa: E731


class Gravador:
    def __init__(self, code=200):
        self.calls, self.code = [], code

    def __call__(self, url, payload, key, *, timeout):
        self.calls.append({"url": url, "payload": payload, "key": key, "timeout": timeout})
        return self.code


class NotificadorCriacaoTest(unittest.TestCase):
    def test_variaveis_da_v2(self):
        self.assertEqual(nc.URL_ENV, "FABRICA_V2_CRIACAO_WEBHOOK_URL")
        self.assertEqual(nc.KEY_ENV, "FABRICA_V2_CRIACAO_WEBHOOK_KEY")
        self.assertFalse(hasattr(nc, "EXPECTED_URL"))

    def test_nao_configurado(self):
        t = Gravador()
        n = nc.notify_creation({"section_name": "feat"}, 0, "e", env={}, user_env_reader=SEM_USER, transport=t)
        self.assertEqual(n["status"], "not_configured")
        self.assertEqual(t.calls, [])

    def test_url_invalida(self):
        t = Gravador()
        n = nc.notify_creation({"section_name": "feat"}, 0, "e", env={nc.URL_ENV: "https://outro.com/x", nc.KEY_ENV: KEY},
                               user_env_reader=SEM_USER, transport=t)
        self.assertEqual(n["status"], "invalid_configuration")
        self.assertEqual(t.calls, [])

    def test_envia_em_sucesso(self):
        t = Gravador()
        n = nc.notify_creation({"section_name": "feat"}, 0, "e1", env=ENV, user_env_reader=SEM_USER, transport=t)
        self.assertEqual(n["status"], "http_accepted")
        self.assertFalse(n["delivery_confirmed"])
        self.assertEqual(t.calls[0]["payload"], {"execution_id": "e1", "script": "criar-secao-feature.py",
                                                 "secao": "feat", "status": "sucesso", "exit": 0, "erro": ""})
        self.assertEqual(t.calls[0]["timeout"], 8)

    def test_envia_em_falha_com_segredo_redigido(self):
        t = Gravador()
        rep = {"section_name": "feat", "message": "erro com " + KEY + " e " + URL}
        n = nc.notify_creation(rep, 3, "e2", env=ENV, user_env_reader=SEM_USER, transport=t)
        self.assertEqual(n["status"], "http_accepted")
        p = t.calls[0]["payload"]
        self.assertEqual((p["status"], p["exit"]), ("falha", 3))
        self.assertNotIn(KEY, json.dumps(p, ensure_ascii=False))
        self.assertNotIn(URL, json.dumps(p, ensure_ascii=False))
        self.assertIn("[redigido]", p["erro"])

    def test_le_variaveis_user(self):
        t = Gravador()
        n = nc.notify_creation({"section_name": "feat"}, 0, "e", env={}, user_env_reader=lambda k: ENV.get(k, ""), transport=t)
        self.assertEqual(n["status"], "http_accepted")


class FluxoCriacaoTest(unittest.TestCase):
    """Roda criar-secao-feature.py de uma cópia temporária (logs não caem em V2\\scripts)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        d = Path(self.tmp.name)
        for nome in ("criar-secao-feature.py", "notificacao_criacao_v2.py"):
            shutil.copy2(ROOT / nome, d / nome)
        (d / "criar-secao-feature.ps1").write_text("# falso\n", encoding="utf-8")
        sys.path.insert(0, str(d))
        for nome in ("criar_secao_feature_tmp", "notificacao_criacao_v2"):
            sys.modules.pop(nome, None)
        spec = importlib.util.spec_from_file_location("criar_secao_feature_tmp", d / "criar-secao-feature.py")
        self.mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.mod)
        self.t = Gravador()
        original = self.mod.notify_creation
        self.mod.notify_creation = lambda rep, code, eid: original(rep, code, eid, env=ENV, user_env_reader=SEM_USER, transport=self.t)
        self.dir = d

    def tearDown(self):
        sys.path.remove(str(self.dir))
        sys.modules.pop("notificacao_criacao_v2", None)
        self.tmp.cleanup()

    def rodar(self, argv):
        out = io.StringIO()
        with redirect_stdout(out):
            code = self.mod.main(argv)
        return code, json.loads(out.getvalue())

    def test_importa_notificador_da_v2(self):
        self.assertIn("notificacao_criacao_v2", (ROOT / "criar-secao-feature.py").read_text(encoding="utf-8"))
        self.assertEqual(self.mod.notify_creation.__class__.__name__, "function")

    def falso_run(self, codigo=0, status="CONCLUIDO", excecao=None):
        def run(command, **kw):
            if excecao:
                raise excecao
            caminho = Path(command[command.index("-ResultPath") + 1])
            caminho.write_text(json.dumps({"status": status, "section_id": "section-nova"}), encoding="utf-8")
            return subprocess.CompletedProcess(command, codigo, "", "")
        return run

    def com_run(self, run, argv):
        original = self.mod.subprocess.run
        self.mod.subprocess.run = run
        orig_is_file = Path.is_file
        Path.is_file = lambda p: True if p.name == "powershell.exe" else orig_is_file(p)
        try:
            return self.rodar(argv)
        finally:
            self.mod.subprocess.run = original
            Path.is_file = orig_is_file

    def test_sucesso_envia(self):
        code, out = self.com_run(self.falso_run(), ["feat-a"])
        self.assertEqual(code, 0)
        self.assertEqual(len(self.t.calls), 1)
        self.assertEqual(self.t.calls[0]["payload"]["status"], "sucesso")
        self.assertEqual(out["notification"]["status"], "http_accepted")
        self.assertFalse(out["needs_human_notification"])

    def test_falha_companion_envia(self):
        code, out = self.com_run(self.falso_run(codigo=1, status="ABORTADO"), ["feat-b"])
        self.assertEqual(code, 3)
        self.assertEqual(self.t.calls[0]["payload"]["status"], "falha")
        self.assertTrue(out["needs_human_notification"])

    def test_timeout_envia(self):
        code, out = self.com_run(self.falso_run(excecao=subprocess.TimeoutExpired("ps", 90)), ["feat-c"])
        self.assertEqual(code, 124)
        self.assertEqual(self.t.calls[0]["payload"]["exit"], 124)
        self.assertEqual(self.t.calls[0]["payload"]["secao"], "feat-c")

    def test_interrupcao_envia(self):
        code, out = self.com_run(self.falso_run(excecao=KeyboardInterrupt()), ["feat-d"])
        self.assertEqual(code, 130)
        self.assertEqual(self.t.calls[0]["payload"]["status"], "falha")

    def test_erro_de_validacao_envia(self):
        code, out = self.rodar(["feat-e", "--selectors", "x.json"])
        self.assertEqual(code, 3)
        self.assertEqual(len(self.t.calls), 1)
        self.assertEqual(self.t.calls[0]["payload"]["status"], "falha")

    def test_nome_invalido_nao_envia(self):
        code, out = self.rodar(["   "])
        self.assertEqual(code, 3)
        self.assertEqual(self.t.calls, [])
        self.assertEqual(out["notification"]["status"], "not_sent_invalid_section")


if __name__ == "__main__":
    unittest.main()