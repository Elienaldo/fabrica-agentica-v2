#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes puros do aviso da V2 ao Bootstrapper (destruição). Sem rede: env e transport falsos."""
from __future__ import annotations

import importlib.util
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import notificacao_bootstrapper as nb  # noqa: E402

spec = importlib.util.spec_from_file_location("destruir_secao_api_notif", ROOT / "destruir-secao-api.py")
api = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = api
spec.loader.exec_module(api)

URL = "https://api2.cursor.sh/automations/webhook/teste-falso-123"
KEY = "chave-falsa-segredo-XYZ"
ENV = {nb.URL_ENV: URL, nb.KEY_ENV: KEY}
SEM_USER = lambda nome: ""  # noqa: E731


class Gravador:
    def __init__(self, code=200, falha=None):
        self.calls, self.code, self.falha = [], code, falha

    def __call__(self, url, payload, key, *, timeout):
        self.calls.append({"url": url, "payload": payload, "key": key, "timeout": timeout})
        if self.falha:
            raise self.falha
        return self.code


def bloqueio(stage="preflight", erro="execução real exige --confirmar-bots com o ID do Arquiteto da seção"):
    return {"status": "bloqueado", "erro": erro, "execution_id": "exec-1", "stage": stage,
            "secao": {"id": "section-x", "nome": "feat-teste"},
            "needs_human_notification": True, "motivos_aviso_humano": [erro]}


class NotificadorTest(unittest.TestCase):
    def test_nao_configurado(self):
        t = Gravador()
        r = bloqueio()
        n = nb.notify_bloqueio_inicial(r, 2, "exec-1", env={}, user_env_reader=SEM_USER, transport=t)
        self.assertEqual(n["status"], "not_configured")
        self.assertFalse(n["delivery_confirmed"])
        self.assertEqual(t.calls, [])
        self.assertIs(r["notification"], n)

    def test_le_variaveis_user_quando_falta_no_processo(self):
        t = Gravador()
        n = nb.notify_bloqueio_inicial(bloqueio(), 2, "exec-1", env={},
                                       user_env_reader=lambda nome: ENV.get(nome, ""), transport=t)
        self.assertEqual(n["status"], "http_accepted")
        self.assertEqual(len(t.calls), 1)

    def test_url_invalida(self):
        for url in ("http://api2.cursor.sh/automations/webhook/x", "https://exemplo.com/automations/webhook/x",
                    "https://api2.cursor.sh/automations/webhook/x/../y"):
            t = Gravador()
            n = nb.notify_bloqueio_inicial(bloqueio(), 2, "exec-1", env={nb.URL_ENV: url, nb.KEY_ENV: KEY},
                                           user_env_reader=SEM_USER, transport=t)
            self.assertEqual(n["status"], "invalid_configuration")
            self.assertEqual(t.calls, [])

    def test_chave_com_quebra_de_linha_invalida(self):
        t = Gravador()
        n = nb.notify_bloqueio_inicial(bloqueio(), 2, "e", env={nb.URL_ENV: URL, nb.KEY_ENV: "a\nb"},
                                       user_env_reader=SEM_USER, transport=t)
        self.assertEqual(n["status"], "invalid_configuration")
        self.assertEqual(t.calls, [])

    def test_so_envia_no_bloqueio_preflight(self):
        casos = [({"status": "sucesso", "stage": "concluido"}, 0),
                 ({"status": "dry-run", "stage": "preflight"}, 0),
                 ({"status": "falha", "stage": "preflight", "erro": "x"}, 1),
                 ({"status": "falha", "stage": "excluir-bots", "erro": "x"}, 1),
                 (bloqueio(stage="listar-secao"), 2)]
        for r, code in casos:
            t = Gravador()
            self.assertIsNone(nb.notify_bloqueio_inicial(r, code, "e", env=ENV, user_env_reader=SEM_USER, transport=t))
            self.assertEqual(t.calls, [])
            self.assertNotIn("notification", r)

    def test_payload_correto_e_uma_vez(self):
        t = Gravador()
        r = bloqueio()
        n = nb.notify_bloqueio_inicial(r, 2, "exec-1", env=ENV, user_env_reader=SEM_USER, transport=t)
        nb.notify_bloqueio_inicial(r, 2, "exec-1", env=ENV, user_env_reader=SEM_USER, transport=t)
        self.assertEqual(len(t.calls), 1)
        c = t.calls[0]
        self.assertEqual(c["url"], URL)
        self.assertEqual(c["timeout"], 8)
        self.assertEqual(c["payload"], {
            "execution_id": "exec-1", "script": "destruir-secao-api.py", "feature": "feat-teste", "exit": 2,
            "erro": r["erro"], "motivos_aviso_humano": [r["erro"]], "status": "aguardando_humano"})
        self.assertEqual(n["status"], "http_accepted")
        self.assertEqual(n["http_status"], 200)
        self.assertEqual(n["attempt_count"], 1)
        self.assertFalse(n["delivery_confirmed"])

    def test_http_rejeitado_e_falha_de_envio(self):
        n = nb.notify_bloqueio_inicial(bloqueio(), 2, "e", env=ENV, user_env_reader=SEM_USER, transport=Gravador(403))
        self.assertEqual(n["status"], "http_rejected")
        n = nb.notify_bloqueio_inicial(bloqueio(), 2, "e", env=ENV, user_env_reader=SEM_USER,
                                       transport=Gravador(falha=OSError("rede")))
        self.assertEqual(n["status"], "send_failed")
        self.assertEqual(n["error_type"], "OSError")

    def test_segredo_redigido(self):
        t = Gravador()
        erro = "falhou com " + KEY + " em " + URL
        r = bloqueio(erro=erro)
        nb.notify_bloqueio_inicial(r, 2, "e", env=ENV, user_env_reader=SEM_USER, transport=t)
        texto = json.dumps(t.calls[0]["payload"], ensure_ascii=False)
        self.assertNotIn(KEY, texto)
        self.assertNotIn(URL, texto)
        self.assertIn("[redigido]", texto)
        self.assertEqual(r["erro"], erro)  # erro original intacto
        self.assertNotIn(KEY, json.dumps(r["notification"]))

    def test_cabecalhos_do_post_real_sem_rede(self):
        capturado = {}

        class Abridor:
            def open(self, request, timeout):
                capturado["headers"] = dict(request.header_items())
                capturado["timeout"] = timeout
                raise OSError("sem rede no teste")

        original = nb.urllib.request.build_opener
        nb.urllib.request.build_opener = lambda *h: Abridor()
        try:
            n = nb.notify_bloqueio_inicial(bloqueio(), 2, "e", env=ENV, user_env_reader=SEM_USER)
        finally:
            nb.urllib.request.build_opener = original
        self.assertEqual(n["status"], "send_failed")
        self.assertEqual(capturado["headers"]["Authorization"], "Bearer " + KEY)
        self.assertEqual(capturado["headers"]["X-automation-key"], KEY)
        self.assertEqual(capturado["timeout"], 8)


class IntegracaoDestruicaoTest(unittest.TestCase):
    """Desde 17/11/2026 o chamador do script é o Bootstrapper: o script não envia aviso por webhook."""

    def rodar(self, argv, client=None):
        with tempfile.TemporaryDirectory() as tmp:
            out = io.StringIO()
            with redirect_stdout(out):
                code = api.main(argv + ["--log-dir", tmp], client=client)
            log = (Path(tmp) / "destruir-secao-api.jsonl").read_text(encoding="utf-8").splitlines()
        return code, json.loads(out.getvalue()), [json.loads(x) for x in log]

    def test_bloqueio_preflight_nao_envia_aviso_e_preserva_exit(self):
        with tempfile.TemporaryDirectory() as cfgdir:
            cfg = Path(cfgdir) / "cfg.json"
            cfg.write_text("{}", encoding="utf-8")
            with mock.patch.object(nb, "notify_bloqueio_inicial", side_effect=AssertionError("não deve enviar")), \
                    mock.patch.object(nb, "_post", side_effect=AssertionError("não deve enviar")):
                code, out, log = self.rodar(["--secao-id", "section-x", "--api-real", "--executar",
                                             "--confirmar-exclusao", "section-x", "--confirmar-bots", "a",
                                             "--config", str(cfg)])
        self.assertEqual(code, 2)
        self.assertEqual(out["status"], "bloqueado")
        self.assertTrue(out["erro"].startswith("rota API não liberada"))
        self.assertTrue(out["needs_human_notification"])
        self.assertNotIn("notification", out)
        self.assertFalse(any("notification" in r for r in log))

    def test_bloqueio_preflight_em_executar_sem_aviso(self):
        with mock.patch.object(nb, "notify_bloqueio_inicial", side_effect=AssertionError("não deve enviar")):
            code, out, log = self.rodar(["--secao-id", " "], client=object())
        self.assertEqual(code, 2)
        self.assertEqual(out["stage"], "preflight")
        self.assertNotIn("notification", out)
        self.assertTrue(out["needs_human_notification"])

    def test_script_nao_tem_mais_hook_de_aviso_ao_bootstrapper(self):
        self.assertFalse(hasattr(api, "avisar_bloqueio_inicial"))
        self.assertFalse(hasattr(api, "NOTIFICACAO_OPCOES"))

    def test_codigo_de_saida_independe_de_aviso(self):
        for r, code in (({"status": "falha", "erro": "x", "stage": "excluir-bots"}, 1),
                        ({"status": "sucesso", "erro": "", "stage": "concluido"}, 0),
                        ({"status": "bloqueado", "erro": "x", "stage": "preflight"}, 2),
                        ({"status": "bloqueado", "erro": "x", "stage": "cruzar"}, 2)):
            out = io.StringIO()
            with mock.patch.object(nb, "notify_bloqueio_inicial", side_effect=AssertionError("não deve enviar")), \
                    redirect_stdout(out):
                self.assertEqual(api.emitir_resultado(dict(r), None), code)
            self.assertNotIn("notification", json.loads(out.getvalue()))

if __name__ == "__main__":
    unittest.main()