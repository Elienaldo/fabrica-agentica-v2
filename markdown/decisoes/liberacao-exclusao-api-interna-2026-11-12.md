# Liberação da exclusão por API interna (Stages A e B) e escopo da validação

**Data:** 12/11/2026 (America/Bahia)
**Dono:** Mestre de obras · **Decisão:** Elienaldo (por voz, via Supervisor, 12/11 15:01)

## Autorização
- **Item 1:** usar a sessão do app do Elienaldo para autenticar na API interna/privada do Grok Bot.
- **Item 2:** apagar de verdade SOMENTE bots e seção descartáveis criados para o teste.
- Proibido: tocar seção/bot real da fábrica; expor token. Destruição real continua exigindo nova autorização humana por pedido.

## Estado final
- **Rota de API interna: validada e LIBERADA.** No `destruir-secao-config.json`, bloco próprio `api_interna` com `validated`, `inventory.no_virtualization_verified`, `inventory.complete_sidebar_verified`, `bot_delete.validated` e `section_delete.validated` todos `true`, apontando a evidência dos Stages A e B.
- **Rota pela tela (UIA): NÃO validada, segue travada.** Os campos de topo do config voltaram a `false`; `destruir-secao-feature-uia.ps1` (inalterado) continua exigindo autorização de uso único + prova de abrir-e-cancelar + confirmação pelo nome.

## O que foi decidido/validado
- **Autenticação aprovada:** sessão do próprio app no PC — chave `os_crypt` de `%APPDATA%\Grok Bot\Local State` aberta por DPAPI do usuário, usada para decriptar access token e machine id de `sand-secrets.json`. Chamadas Connect/JSON em `https://api2.cursor.sh/aiserver.v1.GrokBotService/<RPC>`. Token só em memória, nunca impresso, logado nem copiado para fora do PC.
- **Exclusão de bot:** `DeleteGrokBotAgent {id}`. **Exclusão de seção:** não há RPC própria — `UpdateGrokBotUserRuntimeSettings` regrava a lista inteira de seções sem a alvo, preservando as demais exatamente (releitura antes e depois). Seção conta como vazia pela **regra órfão-ciente** (ids que não existem mais na conta não bloqueiam).
- **Stage A (leitura, não-destrutivo):** auth OK; `ListGrokBotAgents` trouxe 12 agents `truncated=false` (12/12 esperados), sem virtualização; seções lidas por `GetGrokBotUserRuntimeSettings`; RPCs confirmadas.
- **Stage B (destrutivo só em descartáveis):** criados 2 bots + 1 seção descartáveis, apagados de verdade; os 12 bots reais e as 3 seções reais ficaram intactos; 21 chamadas HTTP 200; uma tentativa por exclusão; nenhum segredo gravado; nenhuma restauração necessária.
- **Validação escopada por modo:** liberação vale só para a rota API; a rota de tela permanece como antes. Confirmado por testes (`test_escopo_validacao.ps1`, `check_cliente_escopo.py`) e pela suíte existente.

## Guardas mantidas
- Destruição real exige autorização humana explícita de alvo e escopo, por pedido.
- Bots fixos (Supervisor, Dev Expresso, Âncora, dr eggbot, Mestre de obras) e seções protegidas (Fábrica Agêntica, Uso Pessoal) recusados por id e nome.
- Uma tentativa por exclusão, sem retry. Nunca expor token.

## Pendência / decisão aberta
- O que fazer com a **rota de tela (UIA)**, não validada: validar, bloquear de vez, ou promover a API como rota única. Aguardando decisão do Elienaldo.

## Artefatos atualizados (hashes SHA256, 8 primeiros)
- Biblioteca carregável (box): `arquiteto-regras/SKILL.md` — BF11FE08 → D064553B.
- Espelho (PC): `skills\arquiteto-regras.md` — 1FC294F5 → F0B35C5B. Bloco da seção 24 idêntico ao box (E18F192556).
- `destruir-secao-config.json`, scripts (`destruir-secao-api.py`, `grokbot_api_client.py`) e testes: ver hashes em `RELATORIO-stageB.md` e backups `*.pre-stageB` / `*.pre-escopo`.
- Evidências: `diagnostico-apiinterna-stageA-1112\`, `diagnostico-apiinterna-stageB-1112\`.
- `markdown\modelos\supervisor.md` e a descrição do Supervisor NÃO carregam esse trecho — não alterados.


## Atualizacao — 12/11/2026 15:31 Bahia (decisao final da rota)
Elienaldo escolheu a opcao (c): a rota de API interna passa a ser a UNICA rota de destruicao e a rota pela tela (UIA) foi APOSENTADA.

- Rota de API interna: unica rota, validada e liberada (bloco `api_interna` do config).
- Rota de tela (UIA): aposentada; config com `ui_route_status: aposentada_2026-11-12` e `rota_unica: api_interna` (campos de topo seguem validated=false); o script `destruir-secao-feature-uia.ps1` aborta de inicio em qualquer modo.
- Regra atualizada junto da biblioteca (regra de ouro): arquiteto-regras §24 no box e no espelho do PC, bloco identico. Após a divisão em camadas (12/11/2026), a seção 24 está na skill `arquiteto-destruicao` (espelho `skills\arquiteto-destruicao.md`).
- Nenhuma secao ou bot real foi excluido nesta mudanca.

## Atualização — 13/11/2026 15:20 Bahia (etapa 6: grupos da feature)
Elienaldo aprovou implementar a exclusão dos grupos de chat da feature pela rota de API, logo após bots e seção.
- Implementado em `destruir-secao-api.py` (`etapa6_planejar_grupos`, `etapa6_excluir_grupos_da_feature`, `--confirmar-grupos`) e `grokbot_api_client.py` (`delete_room`, guarda `room_delete`). Regras em `contratos\contrato-destruicao-api-interna.md`, seção "Etapa 6".
- Config: nova capacidade `api_interna.room_delete` com `validated=false` e `validation_evidence=null`. As capacidades `bot_delete` e `section_delete` e o bloco `api_interna` não foram alterados; a rota de bots e seção não passa a exigir `room_delete`.
- Nada foi executado: nenhum teste, dry-run ou chamada à API. Casos novos escritos em `test_destruir_secao_api.py` (classe `Etapa6GruposTests`), não rodados.
- Biblioteca: item 8 na seção 24 de `arquiteto-destruicao` (espelho `skills\arquiteto-destruicao.md` atualizado; skill do box com versão nova gerada para aplicação, pendente).
- Pendência: teste descartável autorizado para comprovar o RPC de grupo antes de qualquer liberação.
