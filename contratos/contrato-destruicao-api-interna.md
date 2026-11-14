# Contrato — destruição de seção por API interna (ideia aprovada)

**Status:** ideia aprovada pelo Elienaldo em 11/11/2026 (por voz). **Implementada** em `destruir-secao-api.py --api-real` + `grokbot_api_client.py`; bots e seção validados em 12/11/2026 (Stages A e B, bloco `api_interna` do config) e rota de API interna promovida a rota única em 12/11/2026 (rota UI aposentada). Etapa 6 (grupos) validada em 13/11/2026 (ver abaixo).

## Objetivo
Excluir os bots de uma seção da feature e depois a própria seção, sem depender da interface visual, usando o backend privado do app Grok Bot (`aiserver.v1.GrokBotService`, protocolo Connect/JSON, `https://api2.cursor.sh`).

## Entrada
Manifesto no formato já usado pelo fluxo de UI:
```json
{"secao":{"nome":"Seção teste","id":"section-mwcoucz9-1"},
 "bots":[{"nome":"Cirurgião","id":"8fb42bc5-..."},{"nome":"Advogado do Diabo","id":"3d5f33df-..."}]}
```
Mais a confirmação explícita do nome da seção e a autorização única (hash do manifesto), como no fluxo atual.

## Fluxo
1. **Ler bots da conta:** `ListGrokBotAgents {}` → `agents[]` com `agentId` (UUID), `id` (numérico), `name`, `kind`. A resposta **não** traz seção.
2. **Ler seções:** `GrokBotSidebarSections` (configurações do usuário, campo `GROK_BOT_USER_SETTINGS_FIELD_SIDEBAR_SECTIONS`) → `sections[] {id, name, agent_ids[]}`. RPC exata de leitura a confirmar (candidata: `GetGrokBotUserRuntimeSettings`).
3. **Cruzar:** localizar a seção pelo `id` do manifesto e conferir o nome. O alvo é a interseção `agent_ids da seção` ∩ `bots do manifesto` ∩ `bots existentes na conta` (nome e UUID batendo).
4. **Excluir bots:** para cada alvo, `DeleteGrokBotAgent {id: <agentId>}`, **uma tentativa por bot**, sem retry. Registrar o resultado de cada chamada.
5. **Reverificar:** reler bots e seção; a seção precisa estar vazia.
6. **Excluir a seção vazia pelo id:** não há RPC dedicada a seção no esquema conhecido; a candidata é regravar as configurações sem essa seção (`UpdateGrokBotUserRuntimeSettings` com o campo SIDEBAR_SECTIONS). A confirmar antes de implementar.
7. **Notificar** a receptora "Fábrica — bloqueio destruição" com `execution_id`, como no contrato atual.

## Guardas (obrigatórias)
- Aborta se: seção protegida (Fábrica Agêntica, Uso Pessoal); bot protegido (Âncora, Supervisor, dr eggbot, Mestre de obras) no alvo; id ou nome da seção divergente; bot do manifesto ausente ou homônimo ambíguo; bot na seção que não está no manifesto (não exclui sobras sem decisão).
- Uma tentativa por bot; falha ou estado incerto para tudo e mantém a seção.
- Seção só é excluída depois de confirmada vazia.
- Execução só com autorização humana explícita de alvo e escopo, como na seção 24 de `supervisor-destruicao`.
- Nunca imprime ou registra token, cookies ou headers.

## Gravação de eventos de token (especificação, 11/11/2026)
A cada chamada à API interna (`ListGrokBotAgents`, `GrokBotSidebarSections`, `DeleteGrokBotAgent` e a exclusão da seção vazia) e a cada fase do fluxo, o script grava **um evento** num arquivo de log da Fábrica.
- **Arquivo:** `logs\consumo-tokens.jsonl` na raiz da Fábrica (uma linha JSON por evento, só acréscimo, nunca reescreve linhas anteriores).
- **Campos obrigatórios:** `timestamp` (ISO 8601 com fuso), `feature`, `bot` (quem orquestrou/executou), `modelo` (modelo do Cursor ou de IA envolvido; `null` quando a etapa não usa modelo), `fase` (ex.: `plan`, `implement`, `review`, `prod`, `destruicao`), `tokens` (tokens consumidos; `0` em chamada de API sem modelo; `null` quando não medido, nunca estimado sem marcação), `resultado` (`ok`, `falha`, `abortado`, `incerto`).
- **Campos de apoio:** `execution_id`, `etapa` (nome da chamada ou passo do fluxo).
- **Exemplo:** `{"timestamp":"2026-11-11T20:30:00-03:00","feature":"fornecedor","bot":"Supervisor","modelo":null,"fase":"destruicao","etapa":"DeleteGrokBotAgent","tokens":0,"resultado":"ok","execution_id":"..."}`
- **Uso:** este log alimenta o dashboard de consumo da Fábrica, sem depender de login no Cursor.
- **Painel HTML de consumo:** gerado sob demanda a partir de `logs\consumo-tokens.jsonl`, deve incluir um **gráfico de linha** do consumo ao longo do tempo, com **eixo X = horário** (`timestamp`) e **eixo Y = tokens** (`tokens`), destacando o **pico** (maior gasto) com horário, fase, bot e modelo do evento, para identificar rapidamente onde houve o maior gasto. Eventos com `tokens` nulo (não medido) não entram como zero no gráfico: aparecem marcados como não medidos.
- **Guardas:** nunca grava token de autenticação, cookies, headers nem conteúdo de prompts; falha ao gravar o log não dispara retry da chamada nem muda o resultado da destruição, só registra a pendência.

## Riscos e pendências antes de implementar
- **Conflito com regra vigente:** hoje a Fábrica proíbe usar API interna e as credenciais do app em `C:\Users\Elienaldo\.grokbot`. Implementar exige que o Elienaldo altere essa regra explicitamente (e a biblioteca do Supervisor junto).
- **API privada e sem documentação oficial:** pode mudar em qualquer atualização do app (a própria equipe da Cursor diz que não há API pública).
- **Autenticação no Windows:** das ferramentas da comunidade, nenhuma tem login pela sessão do app testado no Windows (BugenZhao: só macOS; Nuncio: só macOS; ScriptedAlchemy lê a sessão do app via DPAPI). Definir a forma de autenticação é pendência aberta.
- **Exclusão de seção:** RPC exata não confirmada.
- Testar primeiro em seção descartável com bots descartáveis.

## Etapa 6 — grupos da feature (13/11/2026)
**Status:** implementação aprovada pelo Elienaldo em 13/11/2026 15:20 Bahia e feita em `destruir-secao-api.py` / `grokbot_api_client.py`; **validada** em 13/11/2026 19:39 Bahia em grupo descartável (`api_interna.room_delete.validated=true`, liberada pelo Elienaldo às 19:36 Bahia).
- **Quando:** só depois da exclusão dos bots e da seção (etapa 5), na mesma execução.
- **Alvo:** itens de `ListGrokBotAgents` com `kind = GROK_BOT_AGENT_KIND_ROOM` e nome exato (NFC, sensível a maiúsculas) `canal-<feature>`, `<fase>-<feature>` (research, plan, implement, review) ou legado `<feature>-AAAAMMDD.<tipo>` (research, review, direção); `<feature>` = nome exato da seção alvo.
- **Guardas:** recusa grupo com membro (`memberAgentIds`) fora dos bots da feature e dos fixos Supervisor, Dr. Eggbot e Dev Expresso, ou com membros desconhecidos; dry-run padrão lista plano e recusados; exclusão só com `--confirmar-grupos "<id>=<nome>,..."` igual ao plano; preflight exige `room_delete` liberada; uma tentativa por grupo, sem retry; releitura pós-exclusão; log sanitizado. Sem `--confirmar-grupos`, os grupos ficam pendentes e o humano é avisado.
- **Fato:** o esquema público (BugenZhao/grokbot-cli) modela grupo como `GrokBotAgent` de `kind` ROOM e não tem `DeleteGrokBotRoom`. **Validado (13/11/2026):** `DeleteGrokBotAgent {id: <id do room>}` excluiu o grupo descartável `9bff04c4-1b53-4285-a8fa-4643c15fb94b` (HTTP 200) sem afetar os demais agentes, incluindo o membro; `ListGrokBotAgents` devolveu o room com `memberAgentIds`. Seções: só leitura pós-exclusão, sem snapshot prévio.
- **Evidência:** `C:\Users\Elienaldo\GrokBot-Scripts\diagnostico-apiinterna-stage6-1113\` (RESUMO-stage6.md, verif-delete-room.json, agents-antes.json, agents-apos-delete.json, eventos.jsonl, chamadas.jsonl, settings-apos-delete.json); script `stage6_teste_room_delete.py`. Exclusão real de grupos segue exigindo autorização humana do pedido e `--confirmar-grupos`. Não há modo só-grupos: a etapa 1 exige a seção existente.

## Referências
- Esquema e docs: BugenZhao/grokbot-cli (`schema/services.txt`, `schema/aiserver.proto`); Nuncio-hq/grokbot-cli (`grokbot-core/src/agents.ts`, `server-transport.ts`); ScriptedAlchemy/grok-bot-cli.
- Fluxo vigente: `contrato-webhook-destruicao.md`.
