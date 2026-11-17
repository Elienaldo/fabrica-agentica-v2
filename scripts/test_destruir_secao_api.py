#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Testes unitários com dados simulados. Não chamam API real nem leem credenciais."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import importlib.util

spec = importlib.util.spec_from_file_location(
    "destruir_secao_api",
    ROOT / "destruir-secao-api.py",
)
mod = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = mod
spec.loader.exec_module(mod)

SEC = "section-feat-teste-1"
A = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaa1"
B = "bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbb2"
C_OTHER = "cccccccc-cccc-cccc-cccc-ccccccccccc3"
BOOT = "f99cfa31-bd1e-4687-a134-e31c3e7444f9"
ARQ = "abababab-0000-0000-0000-00000000000a"


def client_base():
    return mod.FixtureClient(
        agents=[
            mod.Agent(A, "Cirurgião da feature"),
            mod.Agent(B, "Advogado da feature"),
            mod.Agent(C_OTHER, "Bot de outra seção"),
            mod.Agent(BOOT, "Bootstrapper"),
            mod.Agent(ARQ, "Arquiteto"),
        ],
        sections=[
            mod.Section(SEC, "fix-fornecedores-layout-prototipo", [ARQ]),
            mod.Section("section-outra", "outra-feature", [C_OTHER]),
            mod.Section("section-fabrica", "Fábrica Agêntica", []),
        ],
    )


class DestruirSecaoApiTests(unittest.TestCase):
    def test_cruzamento_so_bots_da_secao(self):
        c = client_base()
        section = mod.etapa1_ids_da_secao(c, SEC)
        agents = mod.etapa2_lista_geral(c)
        plan = mod.etapa3_cruzar(section, agents)
        self.assertIsNone(plan.bloqueio)
        self.assertEqual({a.agent_id for a in plan.alvos}, {ARQ})
        self.assertNotIn(C_OTHER, {a.agent_id for a in plan.alvos})

    def test_secao_inexistente_bloqueia(self):
        c = client_base()
        result = mod.executar(
            secao_id="section-nao-existe",
            client=c,
            executar_real=False,
            confirmar_exclusao=None,
            confirmar_bots=[],
            log_dir=None,
        )
        self.assertEqual(result["status"], "bloqueado")
        self.assertEqual(mod.codigo_saida(result), 2)

    def test_secao_protegida_bloqueia(self):
        c = client_base()
        result = mod.executar(
            secao_id="section-fabrica",
            client=c,
            executar_real=False,
            confirmar_exclusao=None,
            confirmar_bots=[],
            log_dir=None,
        )
        self.assertEqual(result["status"], "bloqueado")
        self.assertIn("protegida", result["erro"].lower())
        self.assertEqual(c.delete_agent_calls, [])
        self.assertEqual(c.delete_section_calls, [])

    def test_bootstrapper_na_secao_bloqueia_e_fica_intacto(self):
        c = client_base()
        sec = [s for s in c.list_sections() if s.section_id == SEC][0]
        c.sections[sec.key()].agent_ids = [ARQ, BOOT]
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[ARQ, BOOT],
            log_dir=None,
        )
        self.assertEqual(result["status"], "bloqueado")
        self.assertIn("bootstrapper", result["erro"].lower())
        self.assertEqual(c.delete_agent_calls, [])
        self.assertEqual(c.delete_section_calls, [])
        self.assertIn(mod.norm_id(BOOT), c.agents)

    def test_bootstrapper_por_nome_com_outro_id_bloqueia(self):
        c = client_base()
        outro = "dddddddd-dddd-dddd-dddd-ddddddddddd4"
        c.agents[mod.norm_id(outro)] = mod.Agent(outro, " Bootstrapper ")
        c.sections[mod.norm_id(SEC)].agent_ids = [ARQ, outro]
        result = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                              confirmar_bots=[ARQ, outro], log_dir=None)
        self.assertEqual(result["status"], "bloqueado")
        self.assertEqual(c.delete_agent_calls, [])
        self.assertFalse(mod.eh_protegido(mod.Agent(outro, "bootstrapper")))

    def test_bootstrapper_em_confirmar_bots_recusa(self):
        c = client_base()
        result = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                              confirmar_bots=[ARQ, BOOT], log_dir=None)
        self.assertEqual(result["status"], "bloqueado")
        self.assertEqual(c.delete_agent_calls, [])
        self.assertEqual(c.delete_section_calls, [])
        self.assertIn(mod.norm_id(BOOT), c.agents)

    def test_dry_run_padrao_nao_exclui(self):
        c = client_base()
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=False,
            confirmar_exclusao=None,
            confirmar_bots=[],
            log_dir=None,
        )
        self.assertEqual(result["status"], "dry-run")
        self.assertEqual(mod.codigo_saida(result), 0)
        self.assertEqual({a["id"] for a in result["alvos"]}, {ARQ})
        self.assertEqual(c.delete_agent_calls, [])
        self.assertEqual(c.delete_section_calls, [])
        self.assertFalse(result["secao_excluida"])

    def test_executar_sem_confirmacao_bloqueia(self):
        c = client_base()
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=None,
            confirmar_bots=[ARQ],
            log_dir=None,
        )
        self.assertEqual(result["status"], "bloqueado")
        self.assertEqual(c.delete_agent_calls, [])

    def test_lista_confirmada_divergente_bloqueia(self):
        c = client_base()
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[B],
            log_dir=None,
        )
        self.assertEqual(result["status"], "bloqueado")
        self.assertIn("Arquiteto", result["erro"])
        self.assertEqual(c.delete_agent_calls, [])

    def test_executar_exclui_bots_e_depois_a_secao(self):
        c = client_base()
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[ARQ],
            log_dir=None,
        )
        self.assertEqual(result["status"], "sucesso")
        self.assertEqual(mod.codigo_saida(result), 0)
        self.assertEqual(set(c.delete_agent_calls), {ARQ})
        self.assertEqual(c.delete_section_calls, [SEC])
        self.assertTrue(result["secao_excluida"])
        self.assertNotIn(C_OTHER, c.delete_agent_calls)

    def test_falha_de_um_bot_nao_exclui_secao_e_sem_retry(self):
        c = client_base()
        c.fail_agent_ids.add(ARQ)
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[ARQ],
            log_dir=None,
        )
        self.assertEqual(result["status"], "falha")
        self.assertEqual(mod.codigo_saida(result), 1)
        self.assertFalse(result["secao_excluida"])
        self.assertEqual(c.delete_section_calls, [])
        self.assertEqual(c.delete_agent_calls.count(ARQ), 1)
        self.assertTrue(any(f["id"] == ARQ for f in result["failed"]))

    def test_nao_exclui_bots_de_outra_secao(self):
        c = client_base()
        mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[ARQ],
            log_dir=None,
        )
        self.assertIn(C_OTHER, {a.agent_id for a in c.list_agents()})
        self.assertNotIn(C_OTHER, c.delete_agent_calls)

    def test_log_nao_guarda_segredos(self):
        c = client_base()
        with tempfile.TemporaryDirectory() as tmp:
            log_dir = Path(tmp)
            result = mod.executar(
                secao_id=SEC,
                client=c,
                executar_real=False,
                confirmar_exclusao=None,
                confirmar_bots=[],
                log_dir=log_dir,
            )
            text = Path(result["log_path"]).read_text(encoding="utf-8")
            self.assertNotIn("authorization", text.lower())
            self.assertNotIn("cookie", text.lower())
            sanitized = mod.sanitizar_log({"authorization": "secret", "ok": 1})
            self.assertEqual(sanitized["authorization"], "[redacted]")
            self.assertEqual(sanitized["ok"], 1)

    def test_cli_dry_run_com_fixture(self):
        c = client_base()
        fixture = {
            "agents": [
                {"agentId": A, "id": "1", "name": "Cirurgião da feature"},
                {"agentId": B, "id": "2", "name": "Advogado da feature"},
            ],
            "sections": [{"id": SEC, "name": "feat-x", "agent_ids": [A, B]}],
        }
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            fx = tmp_path / "fixture.json"
            fx.write_text(json.dumps(fixture), encoding="utf-8")
            code = mod.main(
                ["--secao-id", SEC, "--fixture", str(fx), "--log-dir", str(tmp_path / "logs")]
            )
            self.assertEqual(code, 0)

    def test_cli_executar_sem_fixture_nao_le_credencial_e_bloqueia(self):
        with tempfile.TemporaryDirectory() as tmp:
            code = mod.main(
                [
                    "--secao-id",
                    SEC,
                    "--executar",
                    "--confirmar-exclusao",
                    SEC,
                    "--confirmar-bots",
                    f"{ARQ}",
                    "--log-dir",
                    tmp,
                ]
            )
            self.assertEqual(code, 2)

    def test_orfaos_nao_impedem_exclusao_da_secao(self):
        # Regra órfão-ciente (Stage B 12/11): id inexistente na conta não conta como bot.
        c = client_base()
        sec = [s for s in c.list_sections() if s.section_id == SEC][0]
        c.sections[sec.key()].agent_ids = [ARQ, "deadbeef-dead-dead-dead-deadbeefdead"]
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[ARQ],
            log_dir=None,
        )
        self.assertEqual(result["status"], "sucesso")
        self.assertTrue(result["secao_excluida"])
        self.assertIn("deadbeef-dead-dead-dead-deadbeefdead", result["orfaos"])

    def test_bot_existente_restante_impede_exclusao_da_secao(self):
        c = client_base()
        c.fail_agent_ids = {mod.norm_id(ARQ)}
        result = mod.executar(
            secao_id=SEC,
            client=c,
            executar_real=True,
            confirmar_exclusao=SEC,
            confirmar_bots=[ARQ],
            log_dir=None,
        )
        self.assertNotEqual(result["status"], "sucesso")
        self.assertFalse(result["secao_excluida"])
        self.assertEqual(c.delete_section_calls, [])

    def test_etapa5_orfao_ciente(self):
        c = client_base()
        sec = [s for s in c.list_sections() if s.section_id == SEC][0]
        c.sections[sec.key()].agent_ids = ["deadbeef-dead-dead-dead-deadbeefdead"]
        r = mod.etapa5_excluir_secao_se_vazia(c, SEC)
        self.assertTrue(r["excluida"])
        self.assertEqual(r["orfaos_ignorados"], ["deadbeef-dead-dead-dead-deadbeefdead"])

    # --- Escopo da validação (12/11/2026): rota API lê só o bloco api_interna ---
    def _cfg(self, tmp, dados):
        p = Path(tmp) / "cfg.json"
        p.write_text(json.dumps(dados), encoding="utf-8")
        return p

    def _api_ok(self):
        ev = "stage A+B"
        return {"validated": True, "validation_evidence": ev,
                "bot_delete": {"validated": True, "validation_evidence": ev},
                "section_delete": {"validated": True, "validation_evidence": ev}}

    def test_liberacao_ignora_campos_de_tela(self):
        with tempfile.TemporaryDirectory() as tmp:
            tela_true = {"validated": True, "validation_evidence": "x",
                         "bot_delete": {"validated": True, "validation_evidence": "x"},
                         "section_delete": {"validated": True, "validation_evidence": "x"}}
            p = self._cfg(tmp, tela_true)
            self.assertFalse(mod.liberacao_api_interna(p)[0])
            self.assertFalse(mod.liberacao_api_interna(p, "bot_delete")[0])

    def test_liberacao_api_interna_por_capacidade(self):
        with tempfile.TemporaryDirectory() as tmp:
            api = self._api_ok()
            p = self._cfg(tmp, {"validated": False, "api_interna": api})
            self.assertTrue(mod.liberacao_api_interna(p)[0])
            self.assertTrue(mod.liberacao_api_interna(p, "bot_delete")[0])
            self.assertTrue(mod.liberacao_api_interna(p, "section_delete")[0])
            api["section_delete"]["validated"] = False
            p = self._cfg(tmp, {"api_interna": api})
            self.assertFalse(mod.liberacao_api_interna(p, "section_delete")[0])
            api["section_delete"]["validated"] = True
            api["validation_evidence"] = " "
            p = self._cfg(tmp, {"api_interna": api})
            self.assertFalse(mod.liberacao_api_interna(p)[0])
            p = self._cfg(tmp, {"api_interna": {**self._api_ok(), "validated": "true"}})
            self.assertFalse(mod.liberacao_api_interna(p)[0])

    def test_cli_api_real_executar_bloqueia_sem_bloco_api(self):
        original = mod.build_client
        def proibido(_args):
            raise AssertionError("cliente real não pode ser construído sem liberação")
        mod.build_client = proibido
        try:
            with tempfile.TemporaryDirectory() as tmp:
                p = self._cfg(tmp, {"validated": True, "validation_evidence": "tela"})
                code = mod.main(["--secao-id", SEC, "--api-real", "--executar",
                                 "--confirmar-exclusao", SEC, "--confirmar-bots", f"{ARQ}",
                                 "--config", str(p), "--log-dir", tmp])
                self.assertEqual(code, 2)
        finally:
            mod.build_client = original



# ---- Etapa 6 (grupos da feature), 13/11/2026. Escritos sem execução (proibido rodar testes nesta data).
FEAT = "fix-fornecedores-layout-prototipo"
R_IMPL = "11111111-1111-1111-1111-111111111111"
R_CANAL = "77777777-7777-7777-7777-777777777777"
ARQ2 = "abababab-0000-0000-0000-00000000000b"
ARQ_FORA = "abababab-0000-0000-0000-00000000000c"
R_RES = "22222222-2222-2222-2222-222222222222"
R_LEG = "33333333-3333-3333-3333-333333333333"
R_OUTRA = "44444444-4444-4444-4444-444444444444"
R_INTRUSO = "55555555-5555-5555-5555-555555555555"
R_SEMMEMB = "66666666-6666-6666-6666-666666666666"
ROOM = "GROK_BOT_AGENT_KIND_ROOM"


def client_grupos():
    c = client_base()
    for a in [
        mod.Agent(R_IMPL, f"implement-{FEAT}", kind=ROOM, member_ids=[ARQ]),
        mod.Agent(R_RES, f"research-{FEAT}", kind=ROOM, member_ids=[ARQ]),
        mod.Agent(R_CANAL, f"canal-{FEAT}", kind=ROOM, member_ids=[ARQ]),
        mod.Agent(R_LEG, f"{FEAT}-20261101.review", kind=ROOM, member_ids=[ARQ]),
        mod.Agent(R_OUTRA, "research-outra-feature", kind=ROOM, member_ids=[C_OTHER]),
        mod.Agent(R_INTRUSO, f"plan-{FEAT}", kind=ROOM, member_ids=[ARQ, A]),
        mod.Agent(R_SEMMEMB, f"review-{FEAT}", kind=ROOM, member_ids=None),
    ]:
        c.agents[a.key()] = a
    return c


def pares_plano():
    return [(R_IMPL, f"implement-{FEAT}"), (R_RES, f"research-{FEAT}")]


class Etapa6GruposTests(unittest.TestCase):
    def test_nome_grupo_casamento_exato(self):
        for fase in ("research", "plan", "implement", "review"):
            self.assertEqual(mod.nome_grupo_da_feature(f"{fase}-{FEAT}", FEAT), f"fase:{fase}")
        self.assertIsNone(mod.nome_grupo_da_feature(f"canal-{FEAT}", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"{FEAT}-20261101.direção", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"{FEAT}-20261101.review", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"{FEAT}-20261101.research", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"prod-{FEAT}", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"research-{FEAT}-2", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"Research-{FEAT}", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"grupo-{FEAT}", FEAT))
        self.assertIsNone(mod.nome_grupo_da_feature(f"{FEAT}-2026110.review", FEAT))

    def test_sem_arquiteto_na_secao_recusa_grupo_com_arquiteto(self):
        r = mod.resolver_arquiteto_da_secao([mod.Agent(A, "Cirurgião da feature"), mod.Agent(B, "Advogado da feature")])
        self.assertIsNone(r["id"])
        self.assertIn("nenhum", r["motivo"])
        g = mod.etapa6_planejar_grupos(FEAT, [mod.Agent(R_RES, f"research-{FEAT}", kind=ROOM, member_ids=[ARQ])],
                                       r["id"])
        self.assertEqual(g["plano"], [])
        self.assertEqual(len(g["recusados"]), 1)

    def test_arquiteto_unico_na_secao_aceita_so_ele(self):
        r = mod.resolver_arquiteto_da_secao([mod.Agent(A, "Cirurgião da feature"), mod.Agent(ARQ, " Arquiteto ")])
        self.assertEqual(r["id"], ARQ)
        rooms = [
            mod.Agent(R_RES, f"research-{FEAT}", kind=ROOM, member_ids=[ARQ]),
            mod.Agent(R_IMPL, f"implement-{FEAT}", kind=ROOM, member_ids=[ARQ, ARQ2]),
        ]
        g = mod.etapa6_planejar_grupos(FEAT, rooms, r["id"])
        self.assertEqual([x["id"] for x in g["plano"]], [R_RES])
        self.assertEqual([x["id"] for x in g["recusados"]], [R_IMPL])
        self.assertIsNone(mod.resolver_arquiteto_da_secao([mod.Agent(ARQ, "arquiteto")])["id"])
        self.assertIsNone(mod.resolver_arquiteto_da_secao([mod.Agent(ARQ, "Arquiteto 2")])["id"])

    def test_dois_arquitetos_na_secao_nenhum_fixo(self):
        r = mod.resolver_arquiteto_da_secao([mod.Agent(ARQ, "Arquiteto"), mod.Agent(ARQ2, "Arquiteto")])
        self.assertIsNone(r["id"])
        self.assertIn("mais de um", r["motivo"])
        g = mod.etapa6_planejar_grupos(FEAT, [mod.Agent(R_RES, f"research-{FEAT}", kind=ROOM, member_ids=[ARQ])],
                                       r["id"])
        self.assertEqual(g["plano"], [])
        self.assertEqual(len(g["recusados"]), 1)

    def test_arquiteto_de_outra_secao_nao_conta(self):
        c = client_base()
        c.sections[mod.norm_id(SEC)].agent_ids = [A]
        c.agents[mod.norm_id(ARQ_FORA)] = mod.Agent(ARQ_FORA, "Arquiteto")
        c.sections["section-outra"].agent_ids.append(ARQ_FORA)
        sala = mod.Agent(R_RES, f"research-{FEAT}", kind=ROOM, member_ids=[A, ARQ_FORA])
        c.agents[sala.key()] = sala
        r = mod.executar(secao_id=SEC, client=c, executar_real=False, confirmar_exclusao=None,
                         confirmar_bots=[], log_dir=None)
        self.assertEqual(r["status"], "dry-run")
        self.assertIsNone(r["grupos"]["arquiteto_fixo"]["id"])
        self.assertEqual(r["grupos"]["plano"], [])
        self.assertEqual([x["id"] for x in r["grupos"]["recusados"]], [R_RES])

    def test_dry_run_resolve_arquiteto_da_secao_alvo(self):
        c = client_base()
        r = mod.executar(secao_id=SEC, client=c, executar_real=False, confirmar_exclusao=None,
                         confirmar_bots=[], log_dir=None)
        self.assertEqual(r["grupos"]["arquiteto_fixo"]["id"], ARQ)

    def test_grupo_so_aceita_arquiteto(self):
        for nome in ("FIXOS_POR_ID", "FIXOS_POR_NOME", "MEMBROS_FIXOS_GRUPO", "MEMBROS_LEGADOS_TOLERADOS"):
            self.assertFalse(hasattr(mod, nome))
        agents = [
            mod.Agent("a1111111-0000-0000-0000-000000000001", f"research-{FEAT}", kind=ROOM, member_ids=[ARQ]),
            mod.Agent("a1111111-0000-0000-0000-000000000002", f"plan-{FEAT}", kind=ROOM, member_ids=[ARQ, A]),
            mod.Agent("a1111111-0000-0000-0000-000000000003", f"implement-{FEAT}", kind=ROOM, member_ids=[ARQ, C_OTHER]),
            mod.Agent("a1111111-0000-0000-0000-000000000004", f"review-{FEAT}", kind=ROOM,
                      member_ids=[ARQ, "99999999-9999-9999-9999-999999999999"]),
            mod.Agent("a1111111-0000-0000-0000-000000000005", f"review-{FEAT}", kind=ROOM, member_ids=None),
            mod.Agent("a1111111-0000-0000-0000-000000000006", f"plan-{FEAT}", kind=ROOM, member_ids=[ARQ, BOOT]),
        ]
        r = mod.etapa6_planejar_grupos(FEAT, agents, ARQ)
        self.assertEqual([x["id"] for x in r["plano"]], ["a1111111-0000-0000-0000-000000000001"])
        self.assertEqual(len(r["recusados"]), 5)

    def test_dry_run_lista_plano_e_recusados_sem_excluir(self):
        c = client_grupos()
        r = mod.executar(secao_id=SEC, client=c, executar_real=False, confirmar_exclusao=None,
                         confirmar_bots=[], log_dir=None)
        self.assertEqual(r["status"], "dry-run")
        self.assertEqual({g["id"] for g in r["grupos"]["plano"]}, {R_IMPL, R_RES})
        self.assertEqual({g["id"] for g in r["grupos"]["recusados"]}, {R_INTRUSO, R_SEMMEMB})
        self.assertEqual(r["grupos"]["arquiteto_fixo"]["id"], ARQ)
        self.assertEqual(c.delete_room_calls, [])
        self.assertEqual(c.delete_agent_calls, [])

    def test_sem_confirmar_grupos_nao_exclui_grupos(self):
        c = client_grupos()
        r = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                         confirmar_bots=[ARQ], log_dir=None)
        self.assertEqual(r["status"], "sucesso")
        self.assertEqual(c.delete_room_calls, [])
        self.assertEqual(len(r["grupos"]["pendentes"]), 2)
        self.assertTrue(r["needs_human_notification"])

    def test_confirmar_grupos_divergente_bloqueia_antes_de_tudo(self):
        c = client_grupos()
        r = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                         confirmar_bots=[ARQ], log_dir=None, confirmar_grupos=pares_plano()[:1])
        self.assertEqual(r["status"], "bloqueado")
        self.assertEqual(c.delete_agent_calls, [])
        self.assertEqual(c.delete_room_calls, [])

    def test_liberacao_grupos_travada_bloqueia_no_preflight(self):
        c = client_grupos()
        r = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                         confirmar_bots=[ARQ], log_dir=None, confirmar_grupos=pares_plano(),
                         liberacao_grupos=lambda: (False, "room_delete travada"))
        self.assertEqual(r["status"], "bloqueado")
        self.assertEqual(r["stage"], "preflight")
        self.assertEqual(c.delete_agent_calls, [])

    def test_exclui_grupos_apos_bots_e_secao_sem_retry(self):
        c = client_grupos()
        c.fail_room_ids = {R_RES}
        r = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                         confirmar_bots=[ARQ], log_dir=None, confirmar_grupos=pares_plano())
        self.assertTrue(r["secao_excluida"])
        self.assertEqual(r["status"], "falha")
        self.assertEqual(r["stage"], "excluir-grupos")
        self.assertEqual(sorted(c.delete_room_calls), sorted([R_IMPL, R_RES]))
        self.assertEqual(set(r["grupos"]["removed"]), {R_IMPL})
        self.assertIn(R_CANAL, c.agents)
        self.assertIn(R_LEG, c.agents)
        self.assertIn(R_OUTRA, c.agents)
        self.assertIn(R_INTRUSO, c.agents)

    def test_ordem_arquiteto_antes_da_secao_e_grupos_depois(self):
        c = client_grupos()
        ordem = []
        orig_agent, orig_secao, orig_room = c.delete_agent, c.delete_section, c.delete_room
        def del_agent(i):
            ordem.append(("agent", i))
            return orig_agent(i)
        def del_secao(i):
            ordem.append(("secao", i))
            return orig_secao(i)
        def del_room(i):
            ordem.append(("room", i))
            return orig_room(i)
        c.delete_agent, c.delete_section, c.delete_room = del_agent, del_secao, del_room
        r = mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                         confirmar_bots=[ARQ], log_dir=None, confirmar_grupos=pares_plano())
        self.assertEqual(r["status"], "sucesso")
        self.assertEqual(r["grupos"]["arquiteto_fixo"]["id"], ARQ)
        i_arq = ordem.index(("agent", ARQ))
        i_sec = [k for k, (tipo, _) in enumerate(ordem) if tipo == "secao"][0]
        i_rooms = [k for k, (tipo, _) in enumerate(ordem) if tipo == "room"]
        self.assertLess(i_arq, i_sec)
        self.assertTrue(i_rooms and min(i_rooms) > i_sec)
        self.assertEqual(set(r["grupos"]["removed"]), {R_IMPL, R_RES})


    def test_cli_confirmar_grupos_exige_room_delete(self):
        original = mod.build_client
        def proibido(_args):
            raise AssertionError("cliente real não pode ser construído sem liberação")
        mod.build_client = proibido
        try:
            with tempfile.TemporaryDirectory() as tmp:
                api = {"validated": True, "validation_evidence": "x",
                       "bot_delete": {"validated": True, "validation_evidence": "x"},
                       "section_delete": {"validated": True, "validation_evidence": "x"},
                       "room_delete": {"validated": False, "validation_evidence": None}}
                p = Path(tmp) / "cfg.json"
                p.write_text(json.dumps({"api_interna": api}), encoding="utf-8")
                code = mod.main(["--secao-id", SEC, "--api-real", "--executar",
                                 "--confirmar-exclusao", SEC, "--confirmar-bots", f"{ARQ}",
                                 "--confirmar-grupos", f"{R_IMPL}=implement-{FEAT}",
                                 "--config", str(p), "--log-dir", tmp])
                self.assertEqual(code, 2)
        finally:
            mod.build_client = original


class Etapa4SoArquitetoTests(unittest.TestCase):
    """V2: --confirmar-bots só com o Arquiteto; bloqueios avisam o humano."""

    def _exec(self, c, bots):
        return mod.executar(secao_id=SEC, client=c, executar_real=True, confirmar_exclusao=SEC,
                            confirmar_bots=bots, log_dir=None)

    def _assert_bloqueio_com_aviso(self, c, r, trecho):
        self.assertEqual(r["status"], "bloqueado")
        self.assertEqual(mod.codigo_saida(r), 2)
        self.assertIn(trecho, r["erro"])
        self.assertTrue(r["needs_human_notification"])
        self.assertIn(r["erro"], r["motivos_aviso_humano"])
        self.assertEqual(c.delete_agent_calls, [])
        self.assertEqual(c.delete_section_calls, [])

    def test_so_arquiteto_confirmado_e_na_secao_segue(self):
        c = client_base()
        r = self._exec(c, [ARQ])
        self.assertEqual(r["status"], "sucesso")
        self.assertEqual(c.delete_agent_calls, [ARQ])
        self.assertEqual(c.delete_section_calls, [SEC])
        self.assertFalse(r["needs_human_notification"])
        self.assertEqual(r["motivos_aviso_humano"], [])

    def test_arquiteto_mais_outro_confirmados_bloqueia(self):
        c = client_base()
        self._assert_bloqueio_com_aviso(c, self._exec(c, [ARQ, A]), "exatamente um item")

    def test_outro_bot_sozinho_bloqueia(self):
        c = client_base()
        self._assert_bloqueio_com_aviso(c, self._exec(c, [A]), "não é o Arquiteto")

    def test_secao_com_arquiteto_e_outro_bot_bloqueia_sem_excluir(self):
        c = client_base()
        c.sections[mod.norm_id(SEC)].agent_ids = [ARQ, A]
        self._assert_bloqueio_com_aviso(c, self._exec(c, [ARQ]), "além do Arquiteto")
        c2 = client_base()
        c2.sections[mod.norm_id(SEC)].agent_ids = [ARQ, A]
        self._assert_bloqueio_com_aviso(c2, self._exec(c2, [ARQ, A]), "além do Arquiteto")

    def test_confirmacao_vazia_bloqueia(self):
        c = client_base()
        self._assert_bloqueio_com_aviso(c, self._exec(c, []), "vazio")
        c2 = client_base()
        self._assert_bloqueio_com_aviso(c2, self._exec(c2, ["  "]), "vazio")

    def test_secao_sem_arquiteto_bloqueia(self):
        c = client_base()
        c.sections[mod.norm_id(SEC)].agent_ids = [A]
        r = self._exec(c, [A])
        self._assert_bloqueio_com_aviso(c, r, "nenhum bot")
        self.assertIsNone(r["grupos"]["arquiteto_fixo"]["id"])

    def test_secao_com_dois_arquitetos_bloqueia(self):
        c = client_base()
        arq2 = "abababab-0000-0000-0000-0000000000a2"
        c.agents[mod.norm_id(arq2)] = mod.Agent(arq2, "Arquiteto")
        c.sections[mod.norm_id(SEC)].agent_ids = [ARQ, arq2]
        self._assert_bloqueio_com_aviso(c, self._exec(c, [ARQ]), "mais de um")

    def test_dry_run_sem_arquiteto_liga_aviso(self):
        c = client_base()
        c.sections[mod.norm_id(SEC)].agent_ids = [A]
        r = mod.executar(secao_id=SEC, client=c, executar_real=False, confirmar_exclusao=None,
                         confirmar_bots=[], log_dir=None)
        self.assertEqual(r["status"], "dry-run")
        self.assertTrue(r["needs_human_notification"])
        self.assertIn(r["grupos"]["arquiteto_fixo"]["motivo"], r["motivos_aviso_humano"])


if __name__ == "__main__":
    unittest.main()
