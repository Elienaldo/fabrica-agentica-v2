#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Destruição de seção por API interna (rascunho executável só com cliente injetado/fixture).

Entrada do Bootstrapper: este próprio arquivo (não há wrapper separado). Desde 17/11/2026 o
Bootstrapper dispara e controla o script inteiro; o Arquiteto só o avisa do encerramento
(handoff com seção, Arquiteto e grupos) e não roda este script.

Padrão: dry-run (não exclui). Execução real exige --executar, o mesmo --secao-id
em --confirmar-exclusao e --confirmar-bots com exatamente um item: o ID do
Arquiteto, único bot da seção na V2. O --secao-id vem do handoff do Arquiteto e o
Bootstrapper o valida (ListSections e dry-run) e só executa com a autorização do handoff do
Arquiteto da seção (ou, fora do handoff ou com divergência, depois da confirmação direta do humano).
Cliente: --fixture (simulado) ou --api-real (grokbot_api_client.GrokBotApiClient,
sessão do app no Windows, token só em memória; escrita só com --executar).
Sem nenhum dos dois, o cliente real é recusado e nada é lido.
Liberação da rota API (12/11/2026): lida SÓ do bloco "api_interna" do config
(validated + bot_delete/section_delete com evidência). Os campos de topo do config
são da rota de tela (UIA), que segue travada e não validada.
Regra de seção vazia órfão-ciente (Stage B, 12/11/2026): ids da seção que não
existem mais na conta (bots já excluídos) não contam; a seção está vazia quando
nenhum agentId dela existe na lista atual de bots.

Etapas: (1) IDs da seção, (2) lista geral de bots, (3) cruzamento,
(4) exclusão do Arquiteto, primeiro e único alvo (único bot da seção na V2),
(5) só então exclusão da seção, se o Arquiteto foi excluído com sucesso.
Uma passagem só: uma tentativa por bot, sem retry.
Ordem com o Arquiteto: o Arquiteto NÃO se autoexclui nem roda este script; só o Bootstrapper roda.
O script exclui o Arquiteto na etapa 4 (por isso o ID dele, e só ele, vai em
--confirmar-bots), depois a seção (etapa 5) e por fim os grupos (etapa 6). O ID do
Arquiteto, para a confirmação e para a guarda dos grupos, é resolvido do inventário
lido antes de qualquer exclusão (um único bot de nome exato "Arquiteto" na seção).
Bloqueia antes de qualquer exclusão se: --confirmar-bots vazio, com mais de um item
ou com item que não seja o Arquiteto; seção sem Arquiteto ou com mais de um; seção
com qualquer bot além do Arquiteto. Aviso ao humano: todo bloqueio ou falha sai com
needs_human_notification=true, exit 2 (bloqueio) ou 1 (falha) e o motivo em "erro" e
em "motivos_aviso_humano"; Arquiteto não resolvido (grupos.arquiteto_fixo sem id)
também liga o aviso, inclusive no dry-run. O script não envia aviso por webhook (desde
17/11/2026 o chamador é o próprio Bootstrapper, que não avisa a si mesmo): o
Bootstrapper lê o resultado (exit, stage, removed, erro, motivos_aviso_humano) e avisa o
humano. notificacao_bootstrapper.py não é mais chamado por este script.
Bot protegido: SOMENTE o Bootstrapper (fixo, sempre existe, nunca é alvo), casado por
ID (BOOTSTRAPPER_ID) OU por nome exato "Bootstrapper" (NFC + strip, sensível a
maiúsculas); na seção alvo ou em --confirmar-bots, aborta antes de excluir.
(6) Grupos da feature (13/11/2026, aprovado pelo Elienaldo às 15:20 Bahia): só
depois do Arquiteto e da seção, e só com --confirmar-grupos (pares id=nome iguais ao
plano). Alvo: SOMENTE kind GROK_BOT_AGENT_KIND_ROOM com nome exato (NFC, sensível
a maiúsculas) <fase>-<feature>, com <fase> em research, plan, implement ou review e
<feature> = nome exato da seção alvo. O ÚNICO membro aceito nos grupos é o bot de
nome exato "Arquiteto" (NFC + strip, sensível a maiúsculas) dentro da seção alvo,
com o ID resolvido do inventário já lido; qualquer outro membro (inclusive o
Bootstrapper) ou membros desconhecidos recusam o grupo. Nenhum
ou mais de um "Arquiteto" na seção: nenhum membro é aceito e o motivo sai no
resultado; "Arquiteto" fora da seção alvo não conta. Exige a capacidade
api_interna.room_delete. A exclusão de grupos (room_delete, via DeleteGrokBotAgent
{id: <id do room>}) foi validada em 13/11/2026 às 19:39 (Bahia), conforme
contrato-destruicao-api-interna.md, seção "Etapa 6 — grupos da feature". A
exclusão real de grupos exige autorização humana e --confirmar-grupos.
"""
from __future__ import annotations

import argparse
import json
import sys
import unicodedata
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Protocol, Sequence, Set, Tuple

EXIT_OK = 0
EXIT_FALHA = 1
EXIT_BLOQUEADO = 2

# Único bot protegido na destruição: o Bootstrapper (fixo, sempre existe, nunca é alvo).
# Casa por ID OU por nome exato (NFC + strip, sensível a maiúsculas). Não é membro
# aceito de grupo: nos grupos da etapa 6, só o Arquiteto é aceito.
BOOTSTRAPPER_ID = "f99cfa31-bd1e-4687-a134-e31c3e7444f9"
NOME_BOOTSTRAPPER = "Bootstrapper"
SECOES_PROTEGIDAS = {
    "fábrica agêntica",
    "fabrica agentica",
    "fábrica agêntica v2",
    "fabrica agentica v2",
    "uso pessoal",
}


CONFIG_PADRAO = Path(__file__).resolve().parent / "destruir-secao-config.json"
CAPACIDADES_API = ("bot_delete", "section_delete", "room_delete")
# Capacidades exigidas para bots + seção. room_delete só é exigida com --confirmar-grupos,
# para que a etapa 6 travada não bloqueie a rota já validada.
CAPACIDADES_BASE = ("bot_delete", "section_delete")

# Etapa 6 (grupos da feature).
KIND_ROOM = "GROK_BOT_AGENT_KIND_ROOM"
FASES_OFICIAIS = ("research", "plan", "implement", "review")  # markdown\fases\fase-*.md
# Único membro aceito nos grupos: o bot de nome exato "Arquiteto" dentro da seção alvo.
# Não há ID global nem parâmetro externo: o ID é resolvido do inventário já lido (bots
# da seção alvo). Nenhum ou mais de um "Arquiteto" na seção = nenhum membro aceito.
NOME_ARQUITETO = "Arquiteto"


def liberacao_api_interna(config_path: Optional[Path] = None, capacidade: Optional[str] = None):
    """Lê a liberação SÓ do bloco "api_interna" do config (nunca dos campos de topo,
    que são da rota de tela/UIA). Devolve (ok, motivo). Exige validated is True e
    validation_evidence preenchida no bloco e, se pedida, na capacidade."""
    path = Path(config_path) if config_path else CONFIG_PADRAO
    try:
        cfg = json.loads(path.read_bytes().decode("utf-8-sig"))
    except Exception as exc:
        return False, f"config ilegível ({path.name}): {exc}"
    blk = cfg.get("api_interna") if isinstance(cfg, dict) else None
    if not isinstance(blk, dict):
        return False, "config sem bloco api_interna; rota API não liberada"

    def ok(d: Any) -> bool:
        return isinstance(d, dict) and d.get("validated") is True and bool(str(d.get("validation_evidence") or "").strip())

    if not ok(blk):
        return False, "api_interna.validated não está true com evidência"
    if capacidade is not None:
        if capacidade not in CAPACIDADES_API:
            return False, f"capacidade desconhecida: {capacidade}"
        if not ok(blk.get(capacidade)):
            return False, f"api_interna.{capacidade}.validated não está true com evidência"
    return True, ""


def nfc_strip(value: str) -> str:
    return unicodedata.normalize("NFC", (value or "").strip())


def norm_id(value: str) -> str:
    return nfc_strip(value).lower()


def norm_nome(value: str) -> str:
    text = nfc_strip(value).casefold()
    text = unicodedata.normalize("NFD", text)
    text = "".join(ch for ch in text if unicodedata.category(ch) != "Mn")
    return " ".join(text.split())


def agora_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


@dataclass
class Agent:
    agent_id: str
    name: str
    numeric_id: Optional[str] = None
    kind: Optional[str] = None
    member_ids: Optional[List[str]] = None  # só rooms; None = desconhecido (recusa na etapa 6)

    def key(self) -> str:
        return norm_id(self.agent_id)

    def copia(self) -> "Agent":
        return Agent(self.agent_id, self.name, self.numeric_id, self.kind,
                     None if self.member_ids is None else list(self.member_ids))


@dataclass
class Section:
    section_id: str
    name: str
    agent_ids: List[str] = field(default_factory=list)

    def key(self) -> str:
        return norm_id(self.section_id)

    def agent_keys(self) -> List[str]:
        return [norm_id(i) for i in self.agent_ids if nfc_strip(i)]


class GrokBotClient(Protocol):
    def list_agents(self) -> List[Agent]:
        ...

    def list_sections(self) -> List[Section]:
        ...

    def delete_agent(self, agent_id: str) -> None:
        ...

    def delete_section(self, section_id: str) -> None:
        ...

    def delete_room(self, room_id: str) -> None:
        ...


class RealApiClientNotAvailable(RuntimeError):
    """Transporte/autenticação reais não estão ligados neste script."""


class RefusedRealApiClient:
    """Recusa qualquer uso da API real e não lê arquivos de credencial."""

    def _blocked(self) -> None:
        raise RealApiClientNotAvailable(
            "Cliente de API real não está ligado neste script. "
            "Autenticação e transporte são pendência; credenciais não são lidas."
        )

    def list_agents(self) -> List[Agent]:
        self._blocked()
        raise AssertionError("unreachable")

    def list_sections(self) -> List[Section]:
        self._blocked()
        raise AssertionError("unreachable")

    def delete_agent(self, agent_id: str) -> None:
        self._blocked()

    def delete_section(self, section_id: str) -> None:
        self._blocked()

    def delete_room(self, room_id: str) -> None:
        self._blocked()


class FixtureClient:
    """Cliente de dados simulados (fixtures / testes). Não acessa rede."""

    def __init__(self, agents: Sequence[Agent], sections: Sequence[Section]):
        self.agents = {a.key(): a.copia() for a in agents}
        self.sections = {s.key(): Section(s.section_id, s.name, list(s.agent_ids)) for s in sections}
        self.delete_agent_calls: List[str] = []
        self.delete_section_calls: List[str] = []
        self.fail_agent_ids: Set[str] = set()
        self.fail_section = False
        self.delete_room_calls: List[str] = []
        self.fail_room_ids: Set[str] = set()

    def list_agents(self) -> List[Agent]:
        return [a.copia() for a in self.agents.values()]

    def list_sections(self) -> List[Section]:
        return [Section(s.section_id, s.name, list(s.agent_ids)) for s in self.sections.values()]

    def delete_agent(self, agent_id: str) -> None:
        key = norm_id(agent_id)
        self.delete_agent_calls.append(key)
        if key in self.fail_agent_ids:
            raise RuntimeError(f"falha simulada ao excluir bot {agent_id}")
        self.agents.pop(key, None)
        for section in self.sections.values():
            section.agent_ids = [i for i in section.agent_ids if norm_id(i) != key]

    def delete_section(self, section_id: str) -> None:
        key = norm_id(section_id)
        self.delete_section_calls.append(key)
        if self.fail_section:
            raise RuntimeError(f"falha simulada ao excluir seção {section_id}")
        section = self.sections.get(key)
        if section is None:
            raise RuntimeError(f"seção não encontrada: {section_id}")
        if [k for k in section.agent_keys() if k in self.agents]:
            raise RuntimeError("seção não está vazia")
        self.sections.pop(key, None)

    def delete_room(self, room_id: str) -> None:
        key = norm_id(room_id)
        self.delete_room_calls.append(key)
        if key in self.fail_room_ids:
            raise RuntimeError(f"falha simulada ao excluir grupo {room_id}")
        room = self.agents.get(key)
        if room is None or room.kind != KIND_ROOM:
            raise RuntimeError(f"grupo não encontrado: {room_id}")
        self.agents.pop(key, None)


def load_fixture(path: Path) -> FixtureClient:
    data = json.loads(path.read_text(encoding="utf-8"))
    agents = [
        Agent(
            agent_id=str(item["agentId"] if "agentId" in item else item["id"]),
            name=str(item.get("name") or ""),
            numeric_id=str(item["id"]) if "agentId" in item and "id" in item else None,
            kind=item.get("kind"),
            member_ids=[str(x) for x in item["memberAgentIds"]] if "memberAgentIds" in item else None,
        )
        for item in data.get("agents", [])
    ]
    sections = [
        Section(
            section_id=str(item["id"]),
            name=str(item.get("name") or ""),
            agent_ids=[str(x) for x in item.get("agent_ids", item.get("agentIds", []))],
        )
        for item in data.get("sections", [])
    ]
    return FixtureClient(agents, sections)


def eh_protegido(agent: Agent) -> bool:
    """Bootstrapper: ID igual a BOOTSTRAPPER_ID OU nome exato "Bootstrapper" (NFC + strip)."""
    return agent.key() == norm_id(BOOTSTRAPPER_ID) or nfc_strip(agent.name) == NOME_BOOTSTRAPPER


def secao_protegida(section: Section) -> bool:
    return norm_nome(section.name) in {norm_nome(n) for n in SECOES_PROTEGIDAS}


def parse_lista_bots(raw: Optional[str]) -> List[str]:
    if not raw:
        return []
    parts: List[str] = []
    for chunk in raw.replace(";", ",").split(","):
        item = nfc_strip(chunk)
        if item:
            parts.append(item)
    return parts


@dataclass
class PlanResult:
    section: Section
    agents_in_account: List[Agent]
    ids_na_secao: List[str]
    alvos: List[Agent]
    orfaos: List[str]
    bloqueio: Optional[str] = None
    protegidos_no_alvo: List[Agent] = field(default_factory=list)


def etapa1_ids_da_secao(client: GrokBotClient, secao_id: str) -> Section:
    wanted = norm_id(secao_id)
    for section in client.list_sections():
        if section.key() == wanted:
            return section
    raise LookupError(f"seção não encontrada: {secao_id}")


def etapa2_lista_geral(client: GrokBotClient) -> List[Agent]:
    return client.list_agents()


def etapa3_cruzar(section: Section, agents: Sequence[Agent]) -> PlanResult:
    by_id = {a.key(): a for a in agents}
    ids_na_secao = section.agent_keys()
    alvos: List[Agent] = []
    orfaos: List[str] = []
    seen: Set[str] = set()
    for key in ids_na_secao:
        if key in seen:
            continue
        seen.add(key)
        agent = by_id.get(key)
        if agent is None:
            orfaos.append(key)
        else:
            alvos.append(agent)
    result = PlanResult(
        section=section,
        agents_in_account=list(agents),
        ids_na_secao=ids_na_secao,
        alvos=alvos,
        orfaos=orfaos,
        protegidos_no_alvo=[a for a in alvos if eh_protegido(a)],
    )
    if secao_protegida(section):
        result.bloqueio = (
            f"seção protegida: {section.name} ({section.section_id})"
        )
        return result
    if result.protegidos_no_alvo:
        nomes = ", ".join(f"{a.name} ({a.agent_id})" for a in result.protegidos_no_alvo)
        result.bloqueio = f"bot protegido (Bootstrapper) no alvo; operação abortada antes de excluir: {nomes}"
        return result
    return result


def etapa4_excluir_bots(client: GrokBotClient, alvos: Sequence[Agent]) -> Dict[str, List[str]]:
    removed: List[str] = []
    failed: List[Dict[str, str]] = []
    for agent in alvos:
        try:
            client.delete_agent(agent.agent_id)
        except Exception as exc:  # uma tentativa, sem retry
            failed.append({"id": agent.agent_id, "nome": agent.name, "erro": str(exc)})
            continue
        removed.append(agent.agent_id)
    return {"removed": removed, "failed": failed}


def ids_existentes_na_secao(section: Section, agents: Sequence[Agent]) -> List[str]:
    """Regra órfão-ciente: só contam ids da seção que existem na conta."""
    existentes = {a.key() for a in agents}
    return [k for k in section.agent_keys() if k in existentes]


def etapa5_excluir_secao_se_vazia(client: GrokBotClient, secao_id: str) -> Dict[str, Any]:
    section = etapa1_ids_da_secao(client, secao_id)
    agents = client.list_agents()
    restantes = ids_existentes_na_secao(section, agents)
    orfaos = [k for k in section.agent_keys() if k not in set(restantes)]
    if restantes:
        return {
            "excluida": False,
            "erro": "seção não está vazia após as exclusões de bots",
            "restantes": restantes,
            "orfaos_ignorados": orfaos,
        }
    try:
        client.delete_section(secao_id)
    except Exception as exc:
        return {"excluida": False, "erro": str(exc), "restantes": [], "orfaos_ignorados": orfaos}
    return {"excluida": True, "erro": None, "restantes": [], "orfaos_ignorados": orfaos}


def nome_grupo_da_feature(nome_grupo: str, feature: str) -> Optional[str]:
    """Devolve "fase:<fase>" se o nome for exatamente <fase>-<feature>, ou None.
    Casamento exato após NFC + strip, sensível a maiúsculas; <fase> em FASES_OFICIAIS;
    <feature> = nome exato da seção."""
    n = nfc_strip(nome_grupo)
    f = nfc_strip(feature)
    if not n or not f:
        return None
    for fase in FASES_OFICIAIS:
        if n == f"{fase}-{f}":
            return f"fase:{fase}"
    return None


def resolver_arquiteto_da_secao(bots_da_secao: Sequence[Agent]) -> Dict[str, Any]:
    """Resolve o único membro fixo dos grupos: o bot (não room) de nome exato "Arquiteto"
    (NFC + strip, sensível a maiúsculas) entre os bots da seção alvo, já lidos do inventário.
    Devolve {"id": <id> ou None, "motivo": ""}. Nenhum ou mais de um: id None e motivo;
    um "Arquiteto" fora da seção alvo não entra porque só os bots da seção são examinados."""
    achados = [a for a in bots_da_secao
               if a.kind != KIND_ROOM and nfc_strip(a.name) == NOME_ARQUITETO]
    if len(achados) == 1:
        return {"id": achados[0].agent_id, "motivo": ""}
    if not achados:
        return {"id": None, "motivo": f'nenhum bot "{NOME_ARQUITETO}" na seção alvo; nenhum membro fixo aceito'}
    return {"id": None, "ids": [a.agent_id for a in achados],
            "motivo": f'mais de um bot "{NOME_ARQUITETO}" na seção alvo; nenhum membro fixo aceito'}


def etapa6_planejar_grupos(feature: str, agents: Sequence[Agent],
                           arquiteto_fixo_id: Optional[str] = None) -> Dict[str, List[Dict[str, Any]]]:
    """Só leitura. Planeja os grupos da feature e lista os recusados (nome casa, mas falha guarda).
    Único membro aceito: arquiteto_fixo_id, vindo de resolver_arquiteto_da_secao (None =
    nenhum membro aceito). Qualquer outro membro, inclusive o Bootstrapper, ou
    member_ids desconhecido, recusa o grupo."""
    fixo = nfc_strip(arquiteto_fixo_id or "")
    permitidos = {norm_id(fixo)} if fixo else set()
    plano: List[Dict[str, Any]] = []
    recusados: List[Dict[str, Any]] = []
    for a in agents:
        if a.kind != KIND_ROOM:
            continue
        padrao = nome_grupo_da_feature(a.name, feature)
        if padrao is None:
            continue
        item = {"id": a.agent_id, "nome": nfc_strip(a.name), "padrao": padrao}
        if eh_protegido(a):
            recusados.append({**item, "motivo": "id/nome protegido"})
        elif a.member_ids is None:
            recusados.append({**item, "motivo": "membros desconhecidos"})
        else:
            fora = [m for m in a.member_ids if nfc_strip(m) and norm_id(m) not in permitidos]
            if fora:
                recusados.append({**item, "motivo": "membro diferente do Arquiteto", "membros_fora": fora})
            else:
                plano.append(item)
    return {"plano": plano, "recusados": recusados}


def parse_lista_grupos(raw: Optional[str]) -> List[Tuple[str, str]]:
    """--confirmar-grupos: pares id=nome separados por vírgula ("" = nenhum grupo)."""
    if raw is None:
        return []
    pares: List[Tuple[str, str]] = []
    for parte in raw.split(","):
        parte = nfc_strip(parte)
        if not parte:
            continue
        if "=" not in parte:
            raise ValueError(f"--confirmar-grupos espera id=nome: {parte}")
        gid, nome = parte.split("=", 1)
        pares.append((nfc_strip(gid), nfc_strip(nome)))
    return pares


def chaves_grupos(pares: Sequence[Tuple[str, str]]) -> Set[Tuple[str, str]]:
    return {(norm_id(i), nfc_strip(n)) for i, n in pares}


def etapa6_excluir_grupos_da_feature(client: GrokBotClient, plano: Sequence[Dict[str, Any]]) -> Dict[str, Any]:
    """Depois de bots e seção. Relê a conta, confere id+nome+kind de cada grupo do plano,
    exclui uma vez (sem retry) e relê para comprovar que sumiu."""
    removed: List[str] = []
    failed: List[Dict[str, str]] = []
    atuais = {a.key(): a for a in client.list_agents()}
    for g in plano:
        a = atuais.get(norm_id(g["id"]))
        if a is None or a.kind != KIND_ROOM or nfc_strip(a.name) != g["nome"]:
            failed.append({"id": g["id"], "nome": g["nome"], "erro": "grupo sumiu ou mudou desde o plano"})
            continue
        try:
            client.delete_room(g["id"])
        except Exception as exc:  # uma tentativa, sem retry
            failed.append({"id": g["id"], "nome": g["nome"], "erro": str(exc)})
            continue
        removed.append(g["id"])
    restantes = {a.key() for a in client.list_agents()}
    for gid in list(removed):
        if norm_id(gid) in restantes:
            removed.remove(gid)
            failed.append({"id": gid, "nome": next(g["nome"] for g in plano if g["id"] == gid),
                           "erro": "releitura: grupo ainda existe"})
    return {"removed": removed, "failed": failed}


SECRET_KEYS = (
    "token", "cookie", "header", "authorization", "secret", "password",
    "set-cookie", "access_token", "refresh_token",
)


def sanitizar_log(payload: Dict[str, Any]) -> Dict[str, Any]:
    def clean(value: Any) -> Any:
        if isinstance(value, dict):
            return {
                k: ("[redacted]" if any(s in k.lower() for s in SECRET_KEYS) else clean(v))
                for k, v in value.items()
            }
        if isinstance(value, list):
            return [clean(v) for v in value]
        return value

    return clean(payload)


def escrever_log(log_dir: Path, record: Dict[str, Any]) -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    path = log_dir / "destruir-secao-api.jsonl"
    line = json.dumps(sanitizar_log(record), ensure_ascii=False, separators=(",", ":"))
    with path.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    return path


def montar_resultado(
    *,
    status: str,
    erro: str,
    execution_id: str,
    secao_id: str,
    dry_run: bool,
    stage: str,
    plan: Optional[PlanResult] = None,
    removed: Optional[List[str]] = None,
    failed: Optional[List[Dict[str, str]]] = None,
    secao_excluida: bool = False,
    log_path: Optional[str] = None,
    grupos: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    alvos = []
    if plan is not None:
        alvos = [{"id": a.agent_id, "nome": a.name} for a in plan.alvos]
        secao = {"id": plan.section.section_id, "nome": plan.section.name}
        ids_na_secao = list(plan.ids_na_secao)
        orfaos = list(plan.orfaos)
        protegidos = [{"id": a.agent_id, "nome": a.name} for a in plan.protegidos_no_alvo]
    else:
        secao = {"id": secao_id, "nome": None}
        ids_na_secao = []
        orfaos = []
        protegidos = []
    # Aviso ao humano (mecanismo existente: needs_human_notification no resultado/log,
    # lido pelo Bootstrapper, que chama o script). Bloqueio/falha, Arquiteto não resolvido na seção
    # (grupos.arquiteto_fixo sem id) e grupos recusados/pendentes ligam o aviso.
    g = grupos or {}
    motivos_aviso: List[str] = []
    if status in {"falha", "bloqueado"}:
        motivos_aviso.append(erro or status)
    arq = g.get("arquiteto_fixo")
    if isinstance(arq, dict) and not arq.get("id"):
        motivos_aviso.append(arq.get("motivo") or "Arquiteto não resolvido na seção alvo")
    if g.get("recusados"):
        motivos_aviso.append("etapa 6: grupos recusados")
    if g.get("pendentes"):
        motivos_aviso.append("etapa 6: grupos pendentes")
    return {
        "status": status,
        "erro": erro or "",
        "execution_id": execution_id,
        "secao": secao,
        "dry_run": dry_run,
        "stage": stage,
        "ids_na_secao": ids_na_secao,
        "alvos": alvos,
        "orfaos": orfaos,
        "protegidos_no_alvo": protegidos,
        "removed": removed or [],
        "failed": failed or [],
        "secao_excluida": secao_excluida,
        "grupos": grupos or {"plano": [], "recusados": [], "removed": [], "failed": [], "pendentes": []},
        "needs_human_notification": bool(motivos_aviso),
        "motivos_aviso_humano": motivos_aviso,
        "log_path": log_path,
    }


def executar(
    *,
    secao_id: str,
    client: GrokBotClient,
    executar_real: bool,
    confirmar_exclusao: Optional[str],
    confirmar_bots: Optional[Sequence[str]],
    log_dir: Optional[Path],
    execution_id: Optional[str] = None,
    confirmar_grupos: Optional[Sequence[Tuple[str, str]]] = None,
    liberacao_grupos: Optional[Callable[[], Tuple[bool, str]]] = None,
) -> Dict[str, Any]:
    execution_id = execution_id or str(uuid.uuid4())
    secao_id = nfc_strip(secao_id)
    dry_run = not executar_real
    stage = "preflight"

    def finish(status: str, erro: str, **kwargs: Any) -> Dict[str, Any]:
        result = montar_resultado(
            status=status,
            erro=erro,
            execution_id=execution_id,
            secao_id=secao_id,
            dry_run=dry_run,
            stage=kwargs.pop("stage", stage),
            **kwargs,
        )
        if log_dir is not None:
            path = escrever_log(log_dir, {"timestamp": agora_iso(), **result})
            result["log_path"] = str(path)
        return result

    if not secao_id:
        return finish("bloqueado", "informe --secao-id", stage="preflight")

    if executar_real:
        if nfc_strip(confirmar_exclusao or "") != secao_id:
            return finish(
                "bloqueado",
                "execução real exige --confirmar-exclusao com o mesmo ID de --secao-id",
                stage="preflight",
            )
        if confirmar_bots is None:
            return finish(
                "bloqueado",
                "execução real exige --confirmar-bots com o ID do Arquiteto da seção",
                stage="preflight",
            )
        if confirmar_grupos is not None and liberacao_grupos is not None:
            ok_g, motivo_g = liberacao_grupos()
            if not ok_g:
                return finish("bloqueado", "etapa 6 (grupos) não liberada: " + motivo_g, stage="preflight")

    try:
        stage = "listar-secao"
        section = etapa1_ids_da_secao(client, secao_id)
        stage = "listar-bots"
        agents = etapa2_lista_geral(client)
        stage = "cruzar"
        plan = etapa3_cruzar(section, agents)
    except LookupError as exc:
        return finish("bloqueado", str(exc), stage=stage)
    except RealApiClientNotAvailable as exc:
        return finish("bloqueado", str(exc), stage=stage)
    except Exception as exc:
        return finish("falha", str(exc), stage=stage)

    if plan.bloqueio:
        return finish("bloqueado", plan.bloqueio, plan=plan, stage="cruzar")

    alvo_ids = [a.agent_id for a in plan.alvos]
    alvo_keys = {norm_id(i) for i in alvo_ids}
    # ID do Arquiteto para a guarda dos grupos: resolvido do inventário lido antes de
    # qualquer exclusão (o Arquiteto é excluído depois, na etapa 4).
    arquiteto_fixo = resolver_arquiteto_da_secao(plan.alvos)
    gplan = etapa6_planejar_grupos(plan.section.name, agents, arquiteto_fixo["id"])
    grupos: Dict[str, Any] = {"plano": gplan["plano"], "recusados": gplan["recusados"],
                              "removed": [], "failed": [], "pendentes": [],
                              "arquiteto_fixo": arquiteto_fixo}

    if executar_real:
        confirmados = [nfc_strip(x) for x in confirmar_bots or []]
        # Etapa 4 na V2: o único alvo é o Arquiteto. Bloqueia antes de qualquer exclusão
        # (com aviso ao humano via needs_human_notification) se a confirmação ou a seção
        # não forem exatamente o Arquiteto.
        arq_id = arquiteto_fixo["id"]
        motivo_arq = ""
        if not [x for x in confirmados if x]:
            motivo_arq = "--confirmar-bots vazio: deve conter só o ID do Arquiteto da seção"
        elif not arq_id:
            motivo_arq = "seção sem Arquiteto único: " + arquiteto_fixo["motivo"]
        else:
            alem = [a for a in plan.alvos if a.key() != norm_id(arq_id)]
            if alem:
                nomes = ", ".join(f"{a.name} ({a.agent_id})" for a in alem)
                motivo_arq = f"seção tem bot além do Arquiteto; nada será excluído: {nomes}"
            elif len(confirmados) != 1:
                motivo_arq = "--confirmar-bots deve ter exatamente um item: o ID do Arquiteto"
            elif norm_id(confirmados[0]) != norm_id(arq_id):
                motivo_arq = "--confirmar-bots não é o Arquiteto da seção"
        if motivo_arq:
            return finish("bloqueado", motivo_arq, plan=plan, grupos=grupos, stage="cruzar")
        confirm_keys = {norm_id(x) for x in confirmados}
        if confirm_keys != alvo_keys:
            return finish(
                "bloqueado",
                "lista confirmada não confere com os bots cruzados da seção",
                plan=plan,
                grupos=grupos,
                stage="cruzar",
            )
        if confirmar_grupos is not None:
            plano_keys = chaves_grupos([(g["id"], g["nome"]) for g in gplan["plano"]])
            if chaves_grupos(confirmar_grupos) != plano_keys:
                return finish(
                    "bloqueado",
                    "lista de grupos confirmada não confere com o plano da etapa 6",
                    plan=plan,
                    grupos=grupos,
                    stage="cruzar",
                )

    if dry_run:
        return finish("dry-run", "", plan=plan, grupos=grupos, stage="cruzar")

    # Etapa 4: exclui o Arquiteto, primeiro e único alvo (único bot da seção na V2).
    # Ele não se autoexclui; quem o exclui é este script, antes da seção.
    stage = "excluir-bots"
    outcome = etapa4_excluir_bots(client, plan.alvos)
    failed = outcome["failed"]
    removed = outcome["removed"]
    if failed:
        return finish(
            "falha",
            "um ou mais bots não foram excluídos; a seção não será excluída",
            plan=plan,
            removed=removed,
            failed=failed,
            grupos={**grupos, "pendentes": list(gplan["plano"])},
            stage="excluir-bots",
        )

    # Etapa 5: só depois do Arquiteto, exclui a seção vazia.
    stage = "excluir-secao"
    sec = etapa5_excluir_secao_se_vazia(client, secao_id)
    if not sec["excluida"]:
        resto = sec.get("restantes") or []
        erro = sec.get("erro") or "seção não excluída"
        if resto:
            erro = f"{erro}: {', '.join(resto)}"
        return finish(
            "falha",
            erro,
            plan=plan,
            removed=removed,
            failed=failed,
            secao_excluida=False,
            grupos={**grupos, "pendentes": list(gplan["plano"])},
            stage="excluir-secao",
        )

    # Etapa 6: grupos da feature, depois da seção, com o plano feito antes das exclusões.
    if confirmar_grupos is None:
        # Sem --confirmar-grupos a etapa 6 não roda: grupos ficam pendentes e o humano é avisado.
        grupos["pendentes"] = list(gplan["plano"])
    elif gplan["plano"]:
        stage = "excluir-grupos"
        gout = etapa6_excluir_grupos_da_feature(client, gplan["plano"])
        grupos["removed"] = gout["removed"]
        grupos["failed"] = gout["failed"]
        if gout["failed"]:
            return finish(
                "falha",
                "um ou mais grupos da feature não foram excluídos (bots e seção já excluídos)",
                plan=plan,
                removed=removed,
                failed=[],
                secao_excluida=True,
                grupos=grupos,
                stage="excluir-grupos",
            )

    return finish(
        "sucesso",
        "",
        plan=plan,
        removed=removed,
        failed=[],
        secao_excluida=True,
        grupos=grupos,
        stage="concluido",
    )


def codigo_saida(result: Dict[str, Any]) -> int:
    status = result.get("status")
    if status in {"sucesso", "dry-run"}:
        return EXIT_OK
    if status == "bloqueado":
        return EXIT_BLOQUEADO
    return EXIT_FALHA


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Exclui os bots de uma seção pelo ID e, só se todos saírem, a seção. "
            "Dry-run é o padrão. API real só com --api-real."
        )
    )
    parser.add_argument("--secao-id", required=True,
                        help="ID da seção alvo, vindo do handoff do Arquiteto e validado pelo Bootstrapper (ex.: section-mwcoucz9-1)")
    parser.add_argument(
        "--executar",
        action="store_true",
        help="Executa exclusões de verdade no cliente informado. Sem esta flag, só planeja (dry-run).",
    )
    parser.add_argument(
        "--confirmar-exclusao",
        default=None,
        help="Obrigatório com --executar; deve ser idêntico a --secao-id.",
    )
    parser.add_argument(
        "--confirmar-bots",
        default=None,
        help=("Obrigatório com --executar; exatamente um item: o ID do Arquiteto da seção (único bot "
              "da seção na V2). Vazio, mais de um item ou outro bot bloqueiam com aviso ao humano."),
    )
    parser.add_argument(
        "--confirmar-grupos",
        default=None,
        help=("Etapa 6, opcional: pares id=nome dos grupos da feature separados por vírgula, "
              "iguais ao plano do dry-run (\"\" = nenhum). Sem ela, grupos não são excluídos. "
              "Exige api_interna.room_delete liberada."),
    )
    parser.add_argument(
        "--fixture",
        default=None,
        help="JSON simulado com agents[] e sections[] (testes/dry-run). Não acessa a API.",
    )
    parser.add_argument(
        "--api-real",
        action="store_true",
        help="Usa a API interna real (grokbot_api_client.py, sessão do app). Escrita só com --executar.",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Config com o bloco api_interna (padrão: destruir-secao-config.json ao lado do script).",
    )
    parser.add_argument(
        "--log-dir",
        default=None,
        help="Pasta de log JSONL, sem segredos. Padrão: logs/ ao lado deste script.",
    )
    return parser


def build_client(args: argparse.Namespace) -> GrokBotClient:
    if args.fixture:
        return load_fixture(Path(args.fixture))
    if getattr(args, "api_real", False):
        sys.path.insert(0, str(Path(__file__).resolve().parent))
        import grokbot_api_client  # noqa: E402

        return grokbot_api_client.GrokBotApiClient(
            allow_destructive=bool(args.executar),
            config_path=Path(args.config) if args.config else None,
        )
    return RefusedRealApiClient()


def default_log_dir() -> Path:
    return Path(__file__).resolve().parent / "logs"


def emitir_resultado(result: Dict[str, Any], log_dir: Optional[Path]) -> int:
    code = codigo_saida(result)
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.write("\n")
    return code


def main(argv: Optional[Sequence[str]] = None, client: Optional[GrokBotClient] = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass
    parser = build_parser()
    args = parser.parse_args(argv)
    log_dir = Path(args.log_dir) if args.log_dir else default_log_dir()
    if client is None and getattr(args, "api_real", False) and args.executar:
        motivos = []
        caps = CAPACIDADES_BASE + (("room_delete",) if args.confirmar_grupos is not None else ())
        for cap in caps:
            ok, motivo = liberacao_api_interna(Path(args.config) if args.config else None, cap)
            if not ok:
                motivos.append(motivo)
        if motivos:
            result = montar_resultado(
                status="bloqueado",
                erro="rota API não liberada: " + "; ".join(motivos),
                execution_id=str(uuid.uuid4()),
                secao_id=nfc_strip(args.secao_id),
                dry_run=False,
                stage="preflight",
            )
            result["log_path"] = str(escrever_log(log_dir, {"timestamp": agora_iso(), **result}))
            return emitir_resultado(result, log_dir)
    used_client = client if client is not None else build_client(args)
    if args.confirmar_bots is not None:
        confirm_bots = parse_lista_bots(args.confirmar_bots)
    elif args.executar:
        confirm_bots = None
    else:
        confirm_bots = []
    try:
        confirm_grupos = parse_lista_grupos(args.confirmar_grupos) if args.confirmar_grupos is not None else None
    except ValueError as exc:
        result = montar_resultado(status="bloqueado", erro=str(exc), execution_id=str(uuid.uuid4()),
                                  secao_id=nfc_strip(args.secao_id), dry_run=not args.executar, stage="preflight")
        result["log_path"] = str(escrever_log(log_dir, {"timestamp": agora_iso(), **result}))
        return emitir_resultado(result, log_dir)
    cfg_path = Path(args.config) if args.config else None
    result = executar(
        secao_id=args.secao_id,
        client=used_client,
        executar_real=bool(args.executar),
        confirmar_exclusao=args.confirmar_exclusao,
        confirmar_bots=confirm_bots,
        log_dir=log_dir,
        confirmar_grupos=confirm_grupos,
        liberacao_grupos=(lambda: liberacao_api_interna(cfg_path, "room_delete"))
        if getattr(args, "api_real", False) else None,
    )
    return emitir_resultado(result, log_dir)


if __name__ == "__main__":
    sys.exit(main())
