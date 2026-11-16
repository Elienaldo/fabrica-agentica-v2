# Contrato — destruição da feature por API interna (V2)

## Script
- **Script real:** `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\destruir-secao-api.py`, com o cliente `grokbot_api_client.py`, a configuração `destruir-secao-config.json` (bloco `api_interna`) e o notificador `notificacao_bootstrapper.py`, na mesma pasta.
- **Backend:** API interna do app Grok Bot (`aiserver.v1.GrokBotService`, protocolo Connect/JSON, `https://api2.cursor.sh`), usando a sessão do app.
- **Log:** `logs\destruir-secao-api.jsonl` ao lado do script (ou `--log-dir`), sem segredos.

## Quem dispara
- O **Arquiteto** dispara o script, informando `--secao-id` (ele está na seção e conhece o ID dela).
- O Arquiteto **não se autoexclui**: quem o exclui é o script, na etapa 4.
- Execução só com autorização humana explícita de alvo e escopo (`arquiteto-destruicao`).

## Parâmetros
- `--secao-id` (obrigatório): ID da seção da feature.
- Sem `--executar`, o script só planeja (dry-run).
- Com `--executar`: `--confirmar-exclusao` idêntico a `--secao-id` e `--confirmar-bots` com exatamente um item, o ID do Arquiteto.
- `--confirmar-grupos "<id>=<nome>,..."`: pares iguais ao plano do dry-run. Sem ele, os grupos não são excluídos e o humano é avisado.
- `--api-real` usa a API interna; `--fixture` usa JSON simulado, sem acessar a API.

## Ordem de exclusão (uma passagem só)
1. Ler a seção (`--secao-id`) e a lista geral de bots (`ListGrokBotAgents`); cruzar os bots da seção com os da conta.
2. **Etapa 4 — Arquiteto:** primeiro e único alvo desta etapa (único bot da seção na V2), por `DeleteGrokBotAgent {id}`.
3. **Etapa 5 — seção:** relida e excluída só se o Arquiteto foi excluído e a seção ficou vazia.
4. **Etapa 6 — grupos da feature:** por último, por `DeleteGrokBotAgent {id do grupo}`.

Uma tentativa por item, sem retry. Falha ou estado incerto para tudo e mantém o que ainda não foi excluído. O ID do Arquiteto, para a confirmação e para a guarda dos grupos, é resolvido do inventário lido antes de qualquer exclusão.

## Bot protegido
- **Somente o Bootstrapper**, reconhecido por ID (`f99cfa31-bd1e-4687-a134-e31c3e7444f9`) ou pelo nome exato `Bootstrapper` (NFC + strip, sensível a maiúsculas).
- Nunca entra nos alvos. Se aparecer no alvo ou em `--confirmar-bots`, a operação aborta antes de qualquer exclusão.
- Seções protegidas (nunca alvo): Fábrica Agêntica e Uso Pessoal.

## Grupos (etapa 6)
- Alvo: itens `kind = GROK_BOT_AGENT_KIND_ROOM` com nome exato `<fase>-<feature>`, com `<fase>` = research, plan, implement ou review e `<feature>` = nome exato da seção. Nenhum outro nome de grupo é alvo.
- **Único membro fixo aceito: o Arquiteto**, pelo nome fixo `Arquiteto`, encontrado na seção da feature. Sem ID global e sem parâmetro externo.
- Grupo com qualquer outro membro (inclusive o Bootstrapper) ou com membros desconhecidos é recusado.
- Nenhum ou mais de um `Arquiteto` na seção: nenhum membro é aceito e o motivo sai em `grupos.arquiteto_fixo`. Um `Arquiteto` fora da seção não conta.
- Exige a capacidade `api_interna.room_delete` liberada.

## Bloqueios e aviso ao humano
- O script bloqueia antes de qualquer exclusão quando:
  - `--confirmar-bots` está vazio;
  - `--confirmar-bots` traz mais de um item ou outro bot que não o Arquiteto;
  - a seção não tem Arquiteto ou tem mais de um;
  - a seção tem qualquer bot além do Arquiteto;
  - a confirmação difere do plano, a seção é protegida ou o ID ou nome da seção diverge.
- Todo bloqueio ou falha sai com `needs_human_notification=true`, exit 2 (bloqueio) ou 1 (falha) e o motivo registrado em `erro` e em `motivos_aviso_humano`.
- Só no bloqueio inicial (exit 2, `stage=preflight`) o script faz um POST de aviso à rotina do **Bootstrapper** "Fábrica V2 — bloqueio destruição", com `erro` e `motivos_aviso_humano`; a rotina só registra e avisa o humano. Nos demais casos não envia nada e o Arquiteto repassa. Detalhes em `contrato-webhook-destruicao.md`.

## Cards de execução
- A exclusão dos cards de execução do Cursor da feature exige autorização humana explícita (regra 32).
- Não é feita pelo `destruir-secao-api.py`.

## Fora deste contrato
- A proteção contra lançamento repetido não se aplica aqui: é regra de `arquiteto-operacao-cursor`.

## Variáveis de ambiente
- `FABRICA_V2_WEBHOOK_URL` e `FABRICA_V2_WEBHOOK_KEY`, lidas por `notificacao_bootstrapper.py` (só no bloqueio inicial). Ainda a configurar pelo humano.
- As variáveis antigas da fábrica anterior seguem só para a V1; a V2 não as lê.

## Segurança
- Nunca imprime nem registra token, cookies ou headers.
