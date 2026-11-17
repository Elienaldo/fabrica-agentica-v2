---
name: Arquiteto — aviso de encerramento ao Bootstrapper
description: >-
  Carregue SOMENTE quando o humano autorizar explicitamente o encerramento da feature: o Arquiteto apenas avisa o Bootstrapper, com o handoff de encerramento. O Arquiteto não exclui nada e não roda o script de destruição.
---
# Arquiteto — aviso de encerramento ao Bootstrapper

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 24. Encerramento da feature: o Arquiteto só avisa o Bootstrapper
Desde 17/11/2026 o encerramento da feature é responsabilidade do Bootstrapper (skill `bootstrapper-encerramento`). O Arquiteto NÃO exclui nada: nem bots (nem a si mesmo), nem a seção, nem os grupos, nem cards ou sessões do Cursor, e NÃO roda `destruir-secao-api.py` nem usa Shell, API interna ou outra rota para isso. Esta regra não concede autorização para excluir e não muda a exceção destrutiva da seção 5 de `arquiteto-regras`.
1. **Gatilho:** somente a autorização humana explícita de encerrar a feature. Fim de fase, merge, produção, conclusão de agente, notificação ou aprovação de finalização, por si só, não são esse gatilho. Na dúvida, pergunte ao humano (seção 26 de `arquiteto-comunicacao-humana`).
2. **Antes de avisar:** registre o texto literal da autorização e a hora (horário da Bahia); envie a mensagem final dos grupos de fase (`markdown\comunicacao.md`, seção 5); junte os ids e nomes exatos dos grupos da feature (`<fase>-<feature>`, fases research, plan, implement e review) que você criou.
3. **Handoff de encerramento ao Bootstrapper** (mensagem direta ao bot Bootstrapper, `f99cfa31-bd1e-4687-a134-e31c3e7444f9`), enxuto e só com estes campos: `feature` (nome exato, igual ao da seção); `secao_id`; `arquiteto_id` (o seu); `grupos` (lista `id=nome`); `autorizacao_texto` (literal); `autorizacao_hora` (Bahia); `escopo` (bots, seção e grupos, ou o que o humano autorizou). O Bootstrapper só aceita o aviso se vier de você (id = `arquiteto_id`, dentro de `secao_id`). Nada de fio de conversa nem de resumos longos (regra 28).
4. **Depois de enviar:** diga ao humano, em uma frase, que o Bootstrapper vai validar o aviso e encerrar a feature (Arquiteto, depois a seção, depois os grupos), sem pedir a confirmação de novo; ele só pergunta se achar alguma divergência. Não envie o handoff de novo, não relance e não faça mais nada de destrutivo: o Bootstrapper pode excluir você a qualquer momento.
5. **A autorização do humano vai no handoff.** O Bootstrapper a aceita sem perguntar de novo só quando o handoff vem de você (o Arquiteto da seção) e passa em todas as travas dele; autorização repassada por qualquer outro bot não vale como aprovação. Por isso `autorizacao_texto` e `autorizacao_hora` têm de ser literais e completos. Se o humano autorizou só parte (por exemplo, só excluir um bot ou manter os grupos), diga isso em `escopo`; um pedido menor não autoriza o encerramento inteiro.
6. Pedido sem autorização inequívoca, duplicata ou notificação nunca gera handoff. Mantenha a feature aberta e avise o humano.
