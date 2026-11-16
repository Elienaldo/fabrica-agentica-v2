#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cliente real (Connect/JSON) da API interna do Grok Bot, autenticado pela sessao do app no Windows.

Autorizacao: Elienaldo, 12/11/2026 (via Supervisor): item 1 = usar a sessao do app para a API.

Seguranca:
- O token e o machine id sao decriptados SO em memoria (DPAPI CurrentUser + AES-256-GCM do
  Chromium OSCrypt), nunca impressos, logados, gravados nem devolvidos em excecoes ou repr.
- NUNCA usa o refresh token (renovar poderia deslogar o app). So o access token.
- Liberacao lida SO do bloco "api_interna" de destruir-secao-config.json (nunca dos campos
  de topo, que sao da rota de tela/UIA): allow_destructive=True exige api_interna.validated;
  delete_agent exige api_interna.bot_delete; delete_section exige api_interna.section_delete;
  delete_room (etapa 6, grupos; 13/11/2026) exige api_interna.room_delete, travada ate teste
  descartavel autorizado. HIPOTESE nao validada: DeleteGrokBotAgent com o id do room.
  O config e relido a cada exclusao.
- Leitura e o padrao. delete_agent/delete_section so funcionam com allow_destructive=True,
  recusam bots fixos e secoes protegidas, e fazem uma tentativa so (sem retry).

Implementa o protocolo GrokBotClient de destruir-secao-api.py (list_agents, list_sections,
delete_agent, delete_section, delete_room).
"""
from __future__ import annotations

import base64
import ctypes
import ctypes.wintypes
import json
import os
import time
import unicodedata
import urllib.error
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

BASE_URL = "https://api2.cursor.sh"
SERVICE = "aiserver.v1.GrokBotService"
RPC_LIST_AGENTS = "ListGrokBotAgents"
RPC_GET_SETTINGS = "GetGrokBotUserRuntimeSettings"
RPC_UPDATE_SETTINGS = "UpdateGrokBotUserRuntimeSettings"
RPC_DELETE_AGENT = "DeleteGrokBotAgent"

FIXOS_POR_ID = {
    "3aa31f55-37e8-46e5-a430-a20b42844084",  # Ancora V2
    "c48d6f40-b5af-48ce-8a00-da7561b3a82a",  # Mestre de obras
    "f99cfa31-bd1e-4687-a134-e31c3e7444f9",  # Bootstrapper
}
SECOES_PROTEGIDAS = {"fabrica agentica", "fabrica agentica v2", "uso pessoal", "unassigned"}
SECOES_PROTEGIDAS_ID = {"section-mvr1ysnu-1", "section-mvfvrsvs-1", "__agents__"}


def _norm_nome(v: str) -> str:
    t = unicodedata.normalize("NFD", (v or "").strip().casefold())
    return " ".join("".join(c for c in t if unicodedata.category(c) != "Mn").split())


class ApiError(RuntimeError):
    """Erro de RPC sem nenhum dado de autenticacao."""


class DestructiveNotAllowed(RuntimeError):
    pass


# ---------- DPAPI (CurrentUser) via ctypes ----------
class _Blob(ctypes.Structure):
    _fields_ = [("cbData", ctypes.wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def _dpapi_unprotect(data: bytes) -> bytes:
    buf = ctypes.create_string_buffer(data, len(data))
    blob_in = _Blob(len(data), ctypes.cast(buf, ctypes.POINTER(ctypes.c_char)))
    blob_out = _Blob()
    ok = ctypes.windll.crypt32.CryptUnprotectData(
        ctypes.byref(blob_in), None, None, None, None, 0, ctypes.byref(blob_out)
    )
    if not ok:
        raise ApiError("DPAPI CryptUnprotectData falhou (sessao de outro usuario Windows?)")
    try:
        return ctypes.string_at(blob_out.pbData, blob_out.cbData)
    finally:
        ctypes.windll.kernel32.LocalFree(blob_out.pbData)


def _app_dir() -> Path:
    return Path(os.environ.get("APPDATA") or Path.home() / "AppData/Roaming") / "Grok Bot"


def _safe_storage_key(app_dir: Path) -> bytes:
    state = json.loads((app_dir / "Local State").read_text(encoding="utf-8"))
    blob = base64.b64decode(state["os_crypt"]["encrypted_key"])
    if blob[:5] != b"DPAPI":
        raise ApiError("Local State sem chave Safe Storage DPAPI")
    return _dpapi_unprotect(blob[5:])


def _decrypt(enc_b64: str, key: bytes) -> str:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM

    raw = base64.b64decode(enc_b64)
    if raw[:3] != b"v10":
        raise ApiError("formato Safe Storage nao suportado")
    return AESGCM(key).decrypt(raw[3:15], raw[15:], None).decode("utf-8").strip()


class _Session:
    """Guarda token/machine id em memoria; repr nao revela nada."""

    __slots__ = ("_token", "_machine_id")

    def __init__(self, token: str, machine_id: str):
        self._token = token
        self._machine_id = machine_id

    def __repr__(self) -> str:
        return "<_Session [redacted]>"

    __str__ = __repr__


def load_app_session(app_dir: Optional[Path] = None) -> _Session:
    app_dir = app_dir or _app_dir()
    secrets = json.loads((app_dir / "sand-secrets.json").read_text(encoding="utf-8"))
    if secrets.get("version") not in (None, 1):
        raise ApiError("versao de sand-secrets.json nao suportada")
    accounts = json.loads(secrets.get("cursor-accounts") or "null") or {}
    active = accounts.get("active")
    acc = (accounts.get("accounts") or {}).get(active) if isinstance(active, str) else None
    if not acc or not acc.get("cursor-access-token"):
        raise ApiError("conta ativa sem access token (abra o app e faca login)")
    key = _safe_storage_key(app_dir)
    token = _decrypt(acc["cursor-access-token"], key)
    machine_id = _decrypt(secrets["cursor-machine-id"], key)
    del key
    if not token:
        raise ApiError("access token vazio")
    return _Session(token, machine_id)


def _app_version(app_dir: Path) -> str:
    try:
        v = json.loads((app_dir / "desktop-status.json").read_text(encoding="utf-8")).get("appVersion")
        return v if isinstance(v, str) and v else "1.0.1"
    except Exception:
        return "1.0.1"


def _checksum(machine_id: str) -> str:
    t = int(time.time() * 1000) // 1_000_000
    b = bytearray((t >> (i * 8)) & 0xFF for i in range(5, -1, -1))
    prev = 165
    for i in range(6):
        b[i] = ((b[i] ^ prev) + i) & 0xFF
        prev = b[i]
    return base64.urlsafe_b64encode(bytes(b)).decode().rstrip("=") + machine_id


class GrokBotApiClient:
    def __init__(self, session: Optional[_Session] = None, *, allow_destructive: bool = False,
                 base_url: str = BASE_URL, timeout: float = 30.0, config_path: Optional[Path] = None):
        self.config_path = config_path
        self._allow_destructive = False
        if allow_destructive:
            self._exigir_liberacao(None)
        self._app_dir = _app_dir()
        self._session = session or load_app_session(self._app_dir)
        self._version = _app_version(self._app_dir)
        self._allow_destructive = bool(allow_destructive)
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.calls: List[Dict[str, Any]] = []  # trilha sem segredos: rpc, http, ok

    def __repr__(self) -> str:
        return f"<GrokBotApiClient allow_destructive={self.allow_destructive} [auth redacted]>"

    def _headers(self) -> Dict[str, str]:
        s = self._session
        return {
            "content-type": "application/json",
            "connect-protocol-version": "1",
            "authorization": "Bearer " + s._token,
            "user-agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                           f"(KHTML, like Gecko) Sand/{self._version} Safari/537.36"),
            "x-cursor-client-type": "sand",
            "x-cursor-client-version": self._version,
            "x-cursor-client-os": "win32",
            "x-cursor-client-source": "sand-desktop",
            "x-sand-box-namespace": "prod",
            "x-ghost-mode": "true",
            "x-cursor-checksum": _checksum(s._machine_id),
            "x-request-id": str(uuid.uuid4()),
        }

    def rpc(self, method: str, body: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.base_url}/{SERVICE}/{method}"
        req = urllib.request.Request(url, data=json.dumps(body).encode("utf-8"),
                                     headers=self._headers(), method="POST")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                status = resp.status
                data = resp.read()
        except urllib.error.HTTPError as e:
            try:
                info = json.loads(e.read().decode("utf-8", "replace"))
                code, msg = info.get("code", ""), info.get("message", "")
            except Exception:
                code, msg = "", ""
            self.calls.append({"rpc": method, "http": e.code, "ok": False, "code": code})
            raise ApiError(f"{method} falhou: HTTP {e.code} {code} {msg}".strip()) from None
        except urllib.error.URLError as e:
            self.calls.append({"rpc": method, "http": None, "ok": False})
            raise ApiError(f"{method} falhou: rede ({e.reason})") from None
        self.calls.append({"rpc": method, "http": status, "ok": True})
        return json.loads(data.decode("utf-8")) if data else {}

    # ---------- leitura ----------
    def list_agents_raw(self) -> Dict[str, Any]:
        return self.rpc(RPC_LIST_AGENTS, {})

    def get_settings_raw(self) -> Dict[str, Any]:
        return self.rpc(RPC_GET_SETTINGS, {})

    def list_agents(self):
        Agent = _destruir_module().Agent
        out = []
        for a in self.list_agents_raw().get("agents", []) or []:
            out.append(Agent(agent_id=str(a.get("agentId") or a.get("id") or ""),
                             name=str(a.get("name") or ""),
                             numeric_id=str(a["id"]) if a.get("agentId") and a.get("id") else None,
                             kind=a.get("kind"),
                             member_ids=([str(x) for x in a["memberAgentIds"]]
                                         if "memberAgentIds" in a else None)))
        return out

    def _sections_raw(self) -> List[Dict[str, Any]]:
        st = (self.get_settings_raw().get("settings") or {})
        return list(((st.get("sidebarSections") or {}).get("sections")) or [])

    def list_sections(self):
        Section = _destruir_module().Section
        return [Section(section_id=str(s.get("id") or ""), name=str(s.get("name") or ""),
                        agent_ids=[str(x) for x in (s.get("agentIds") or [])])
                for s in self._sections_raw()]

    # ---------- escrita (bloqueada por padrao) ----------
    def _exigir_liberacao(self, capacidade: Optional[str]) -> None:
        ok, motivo = _destruir_module().liberacao_api_interna(self.config_path, capacidade)
        if not ok:
            raise DestructiveNotAllowed("rota API nao liberada: " + motivo)

    @property
    def allow_destructive(self) -> bool:
        return self._allow_destructive

    @allow_destructive.setter
    def allow_destructive(self, value: bool) -> None:
        if value:
            self._exigir_liberacao(None)
        self._allow_destructive = bool(value)

    def _guard(self, capacidade: str):
        if not self._allow_destructive:
            raise DestructiveNotAllowed("cliente em modo leitura; allow_destructive=False")
        self._exigir_liberacao(capacidade)

    def delete_agent(self, agent_id: str) -> None:
        self._guard("bot_delete")
        if not (agent_id or "").strip() or (agent_id or "").strip().lower() in FIXOS_POR_ID:
            raise DestructiveNotAllowed("bot fixo/protegido: recusado")
        self.rpc(RPC_DELETE_AGENT, {"id": agent_id})  # uma tentativa, sem retry

    def delete_room(self, room_id: str) -> None:
        """Etapa 6: exclui um grupo (room). Travado por api_interna.room_delete.
        HIPOTESE (esquema publico: room = GrokBotAgent kind ROOM; nao ha DeleteGrokBotRoom):
        DeleteGrokBotAgent {id: <id do room>}. So vale apos teste descartavel autorizado."""
        self._guard("room_delete")
        rid = (room_id or "").strip()
        if not rid or rid.lower() in FIXOS_POR_ID:
            raise DestructiveNotAllowed("grupo vazio/protegido: recusado")
        self.rpc(RPC_DELETE_AGENT, {"id": rid})  # uma tentativa, sem retry

    def build_delete_section_body(self, section_id: str, sections: List[Dict[str, Any]],
                                  existing_agent_ids: Optional[set] = None) -> Dict[str, Any]:
        """Lista inteira menos a secao alvo; demais secoes reenviadas intactas (com orfaos).
        Regra orfao-ciente: com existing_agent_ids, so ids que existem na conta contam."""
        if section_id in SECOES_PROTEGIDAS_ID:
            raise DestructiveNotAllowed("secao protegida (id): recusado")
        alvo = [s for s in sections if str(s.get("id")) == section_id]
        if len(alvo) != 1:
            raise ApiError(f"secao {section_id} nao encontrada (ou duplicada)")
        if _norm_nome(alvo[0].get("name", "")) in SECOES_PROTEGIDAS:
            raise DestructiveNotAllowed("secao protegida: recusado")
        ids = [str(x).lower() for x in (alvo[0].get("agentIds") or [])]
        vivos = ids if existing_agent_ids is None else [i for i in ids if i in existing_agent_ids]
        if vivos:
            raise ApiError("secao nao esta vazia (bots existentes: " + ", ".join(vivos) + ")")
        restantes = [s for s in sections if str(s.get("id")) != section_id]
        return {"sidebarSections": {"sections": restantes}}

    def delete_section(self, section_id: str) -> None:
        self._guard("section_delete")
        existentes = {str(a.get("agentId", "")).lower()
                      for a in (self.list_agents_raw().get("agents") or [])}
        body = self.build_delete_section_body(section_id, self._sections_raw(), existentes)
        self.rpc(RPC_UPDATE_SETTINGS, body)  # regrava SIDEBAR_SECTIONS sem a secao


_DESTRUIR = None


def _destruir_module():
    global _DESTRUIR
    if _DESTRUIR is None:
        import importlib.util
        p = Path(__file__).resolve().parent / "destruir-secao-api.py"
        spec = importlib.util.spec_from_file_location("destruir_secao_api", p)
        mod = importlib.util.module_from_spec(spec)
        import sys
        sys.modules["destruir_secao_api"] = mod
        spec.loader.exec_module(mod)
        _DESTRUIR = mod
    return _DESTRUIR
