# Exclusão dos cards de execução ao encerrar um pedido

**Data:** 2026-11-12 (America/Bahia, UTC-3).
**Estado:** regra registrada e aplicada nos artefatos do Supervisor.
**Escopo desta entrega:** regra nova (seção 32) do Supervisor, gravada na biblioteca carregável (box `supervisor-regras/SKILL.md` e cópia do projeto `skills\supervisor-regras.md`), no modelo `markdown\modelos\supervisor.md` e na descrição do bot Supervisor; mais este registro de decisão. Após a divisão em camadas (12/11/2026), a seção 32 está na skill `supervisor-destruicao` (espelho `skills\supervisor-destruicao.md`). Nenhum card foi excluído por esta entrega.

## Decisão

Assim que o Elienaldo autorizar o encerramento de um pedido/solicitação, o Supervisor exclui TODOS os cards de execução relacionados àquele pedido — os cards criados a cada comunicação com o Cursor, que ficam na atividade de programação. Uma única feature pode gerar quatro ou mais cards de execução.

## Regras

1. Gatilho exclusivo: autorização humana explícita de encerramento daquele pedido. Fim de fase, merge, conclusão de agente, produção ou notificação, por si só, não autorizam excluir os cards.
2. Identificação pelo livro-razão (request_id -> agent_id) e pelo índice da feature; exclui só os cards daquele pedido, com casamento único; nunca cards de outro pedido.
3. Cobre os cards/execuções (atividade de programação do Cursor) do pedido; não é a destruição de seção/bots da seção 24, que mantém guardas e autorização próprias.
4. Apenas meios sancionados. Card que não puder ser excluído, estado incerto ou sem casamento: registrar pendência e avisar o humano, sem rota alternativa destrutiva.

## Artefatos atualizados neste trabalho

- `skills\supervisor-regras.md` (cópia do projeto da biblioteca) — seção 32.
- biblioteca carregável do box `supervisor-regras/SKILL.md` — seção 32.
- `markdown\modelos\supervisor.md` — seção 32.
- descrição do bot Supervisor (perfil) — seção 32.
