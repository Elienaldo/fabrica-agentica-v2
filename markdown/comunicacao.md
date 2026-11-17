# Comunicação da fábrica

**Nome:** Comunicação da fábrica (V2)

**Responsável:** Arquiteto da feature. Ele cria os grupos de fase e é o único bot que fala com o humano durante a feature.

> **OBRIGATÓRIO:** não existe grupo inicial nem grupo de direção. A comunicação da feature é um grupo por fase, `<fase>-<nome-da-feature>`, criado pelo Arquiteto quando a fase começa, só com ele e o humano. O Cursor não entra em grupo.

**Job único:** definir quem fala com quem, em quais grupos do Grok Bot, por onde tudo passa e como os grupos nascem, encerram e são apagados. A visão geral da fábrica está em `modelos/fábrica-agêntica-v2.md`.

**Anti-jobs:** o Arquiteto nunca reaproveita grupo entre features; nunca apaga grupo (quem exclui os grupos da feature é o Bootstrapper, no encerramento, com a autorização do humano que vem no handoff do Arquiteto, depois das travas); nunca coloca o Cursor em grupo; nunca cria grupo de direção ou grupo inicial.

**Voz:** regra imperativa, sem exceção.

**Acordar:** sob demanda, quando uma fase começa.

## 1. Criação dos grupos

1. O Arquiteto cria o grupo da fase quando a fase começa (research, plan, implement ou review), não na criação da seção.
2. Membros: só o Arquiteto e o humano que pediu a feature.
3. Se a feature pula o research, não existe grupo de research.
4. Canais não se aninham.

## 2. Grupos

| Grupo | Membros | Quando existe |
|---|---|---|
| `<fase>-<nome-da-feature>` (research, plan, implement, review) | Arquiteto e o humano | Aberto quando a fase começa |

## 3. Pares de comunicação

| Par | Onde acontece |
|---|---|
| Arquiteto e humano | Grupo da fase em curso |
| Arquiteto e sessões do Cursor | **Fora do Grok Bot**: o Cursor não é agente do Grok Bot, então não entra em grupo. O Arquiteto abre a sessão, e o retorno chega pela notificação de conclusão do agente de nuvem (`automacoes/comunicacao-bidirecional-cursor.md`) |
| Bootstrapper e humano | Só no pedido da feature e nos avisos de bloqueio dos scripts por webhook |

## 4. Roteamento

1. Durante a feature, tudo que vai para o humano passa pelo Arquiteto.
2. A decisão do humano volta pelo mesmo grupo em que a pergunta nasceu.
3. Só o Arquiteto fala com o Cursor.
4. Toda fase nova começa com o Arquiteto solicitando ao Cursor uma sessão nova, com contexto limpo. Nenhuma fase reaproveita a sessão da anterior (regra 28, `arquiteto-fases`).

## 5. Nome dos canais e encerramento

1. Nome padronizado do grupo de fase (decisão do Elienaldo, 13/11/2026): `<fase>-<nome-da-feature>`, por exemplo `research-feat-nome-da-feature` ou `review-feat-nome-da-feature`. O nome da feature é o mesmo que ela recebe ao ser criada, isto é, o nome da seção criada pelo Bootstrapper (prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens). Vale para o grupo de research, o de review e o grupo de qualquer outra fase.
   - Formato anterior dos grupos de fase, substituído em 13/11/2026: `feat-<slug>-AAAAMMDD.<tipo>` (tipo `research` ou `review`).
+
+3. Em seguida os bots saem do canal, deixando um membro. Assim não recebem mais nada.
3. Em seguida os bots saem do canal, deixando um membro. Assim não recebem mais nada.
4. Canal nunca é reaproveitado entre features, porque mistura contexto.

## 6. Histórico

1. Se o grupo não for excluído no encerramento (sem `--confirmar-grupos`), o canal fica arquivado por 30 dias e o humano apaga em lote ou na hora, como preferir.
2. A conversa do canal não vale como histórico. O registro de verdade é a documentação do projeto: ADRs, lições e estado das skills.
3. No ADR existente, acrescenta-se uma única linha com o veredito final da revisão: passou ou não.

**Como concreto:** canais do Grok Bot (criar canal e mudar membros).

**Ciclo de vida:** permanente; vale para toda feature.

## 7. Pontos em aberto (a confirmar com o Elienaldo)

- **Prefixo:** o ditado dizia `fit`; foi gravado `feat`, para casar com a branch `feat/`. Confirmar.
- **Dono do ADR:** quem escreve a linha do veredito não está definido.
