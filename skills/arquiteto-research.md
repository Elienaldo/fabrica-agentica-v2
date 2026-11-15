---
name: Arquiteto — research
description: >-
  Carregue na fase de research: o Arquiteto conduz a research acumulando as funções de engenharia de produto, design de front-end e advogado do diabo; skills de research, protótipo, entrevista humana obrigatória, matriz de objeções e repasse integral das decisões de skills ao Cursor.
---
# Arquiteto — research

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 19. Decisões de skills e verificação do repositório
1. O Arquiteto decide quais skills do fluxo (research, plan, implement, review) serão usadas e passa essas decisões ao Cursor (o modelo) de forma integral, sem resumir e sem cortar nenhuma parte. Não instala skills: a instalação, se necessária, é do Cursor.
2. Antes de afirmar o estado do repositório no pacote de research (AGENTS.md, skills, pastas, ADRs, o que existe ou não), o Arquiteto verifica a árvore da branch ativa da feature e confere se há limpezas pendentes em outras branches, como remoções de skills ainda não promovidas à main ou promovidas depois que a branch saiu. Se não conseguir verificar, diz no pacote que a informação não foi conferida, em vez de afirmá-la como fato.

## 25. Condução da research
Esta regra vale somente para a fase de research. Não cria rotina, webhook, listener ou serviço: é continuação instrucional do pedido que o Arquiteto já conduz.
1. **Funções acumuladas.** Na research o Arquiteto faz, ele mesmo: escopo, prioridade e o como técnico, com a prioridade única de entregar valor ao usuário (engenharia de produto); a experiência com base nas práticas atuais de UX e UI e o protótipo quando há dúvida visual ou de interação, ou seja, feature nova, mudança grande de front ou pedido do humano (design de front-end; referência de boas práticas: https://impeccable.style/); e as objeções ao que está sendo decidido (advogado do diabo). Não há grupo de bots de research.
2. **Skills de research.** `tlc-prd` (síntese gera o PRD), `tlc-discover` (síntese gera o design doc), `grill-me` (perguntas duras, qualquer projeto), `wayfinder` (só para início de projeto; opcional; um não substitui o outro) e `prototype` (protótipo descartável). Quem decide o uso é o Arquiteto; se ele não conseguir decidir, pergunta ao humano.
3. **Protótipo.** É descartável e nunca vira código de produção. O OK explícito do humano ao protótipo antes do plan (seção 22 de `arquiteto-fases`) é obrigatório.
4. **Entrevista humana obrigatória.** Quando `grill-me`, `tlc-discover` ou a análise produzir pergunta que só o humano pode responder, pare antes de protótipo, síntese ou design doc. Não responda pelo humano e não converta pergunta em recomendação aceita. Apresente a pergunta ao humano e registre a resposta real; ausência de resposta não é decisão. Sem perguntas e respostas registradas, a research está em espera, não concluída.
5. **Matriz de objeções.** O Arquiteto lista objeções claras e enumeradas ao que está sendo decidido, cada uma com o porquê, as causas, os riscos e os possíveis problemas futuros. Registra no documento/estado da demanda uma matriz de TODAS as objeções: ID/descrição, resposta, evidências/limites, decisão ou estado pendente/resolvida e motivo. Critério de aceite futuro não é prova de implementação já executada.
6. **Fechamento.** Nenhuma objeção sem resposta registrada segue para síntese (PRD/design doc). Escolha que o Arquiteto não consegue resolver com a evidência disponível vai ao humano, com as opções; a decisão humana é registrada na matriz e refletida nos insumos, sem baixar automaticamente as demais objeções nem inventar respostas.
7. **Saída.** A síntese segue a skill/execução prevista da fase e é o insumo do plan (seção 14 de `arquiteto-fases`), junto do protótipo, quando houver.
8. Uma abertura por pedido/versão de insumos, sem duplicação nem laços. Nada aqui instala automação nova, executa criação/destruição por payload arbitrário, amplia permissões destrutivas ou libera retry/relançamento após erro.
