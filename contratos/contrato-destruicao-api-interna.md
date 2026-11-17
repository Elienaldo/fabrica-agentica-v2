# Contrato — destruição da feature por API interna (V2)

## Script
- **Script real:** `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\destruir-secao-api.py`, com o cliente `grokbot_api_client.py`, e a configuração `destruir-secao-config.json` (bloco `api_interna`), na mesma pasta.
- **Backend:** API interna do app Grok Bot (`aiserver.v1.GrokBotService`, protocolo Connect/JSON, `https://api2.cursor.sh`), usando a sessão do app.
- **Log:** `logs\destruir-secao-api.jsonl` ao lado do script (ou `--log-dir`), sem segredos.

## Quem dispara
- O **Bootstrapper** dispara e controla o script inteiro (skill `bootstrapper-encerramento`). O `--secao-id` vem do handoff de encerramento que o Arquiteto envia ao Bootstrapper; o Bootstrapper o valida por `ListSections` e pelo dry-run.
- O **Arquiteto não exclui nada, nem a si mesmo, e não roda o script**: ele só avisa o Bootstrapper (`arquiteto-destruicao`, seção 24), com o nome da feature, o id da seção, o id do Arquiteto, os ids e nomes dos grupos de fase e o texto e a hora da autorização humana. Quem exclui o Arquiteto é o script, na etapa 4.
- Execução real só depois do dry-run e de uma destas autorizações: (1) o handoff do próprio Arquiteto da seção, que traz `autorizacao_texto` e `autorizacao_hora` e passa em todas as travas abaixo (decisão do Elienaldo em 17/11/2026: o humano já autorizou, o Bootstrapper não pede a confirmação de novo); ou (2) a confirmação direta do humano ao Bootstrapper, com alvo e alcance, obrigatória em pedido que não venha desse handoff (de outro bot, ou do humano fora do fluxo) e em qualquer divergência. A autorização repassada por qualquer outro bot não vale como aprovação.
- Travas do handoff do Arquiteto: (a) o remetente é o bot de id igual a `arquiteto_id` e esse bot está dentro de `secao_id` (conferido por `ListSections`); (b) o dry-run é obrigatório antes de `--api-real --executar`; (c) se houver divergência o Bootstrapper PARA e pergunta ao humano: remetente diferente de `arquiteto_id`, seção que não bate, alvo protegido, alvo além do Arquiteto e dos grupos informados, grupos do dry-run diferentes dos do handoff, `needs_human_notification` verdadeiro ou qualquer campo faltando; (d) a ordem é Arquiteto, seção e grupos, e `--confirmar-grupos` só leva os ids exatos do handoff que batem com o dry-run.

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
- O script não envia aviso por webhook (desde 17/11/2026): como o chamador é o próprio Bootstrapper, ele lê o resultado (exit, `stage`, `removed`, `erro`, `motivos_aviso_humano`) e avisa o humano. Detalhes em `contrato-webhook-destruicao.md`.

## Fora deste contrato
- A proteção contra lançamento repetido não se aplica aqui: é regra de `arquiteto-operacao-cursor`.

## Variáveis de ambiente
- `FABRICA_V2_WEBHOOK_URL` e `FABRICA_V2_WEBHOOK_KEY` não são mais lidas por este script (o aviso por webhook foi retirado; `notificacao_bootstrapper.py` ficou sem chamador).
- As variáveis antigas da fábrica anterior seguem só para a V1; a V2 não as lê.

## Segurança
- Nunca imprime nem registra token, cookies ou headers.
