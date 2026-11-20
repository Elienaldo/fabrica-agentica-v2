# Decisão: subida em dev e prod e pergunta de encerramento logo depois

**Data:** 20/11/2026 (horário da Bahia)
**Pedido de:** Elienaldo
**Executado por:** Mestre de obras

## Problema
Ao fim do teste local, quando o Elienaldo autorizava a subida, o Arquiteto pedia e fazia a instalação só em produção e esquecia o dev. Depois avisava e esperava o humano pedir o encerramento.

## O que foi decidido
1. **Subida autorizada vale para os DOIS ambientes, dev e prod.** Com a confirmação explícita do humano, o Arquiteto pede ao modelo do Cursor (mesma sessão da review, sem sessão nova), no mesmo pedido, a instalação da correção em dev E em prod e acompanha até os dois confirmarem. É proibido pedir ou fazer só prod, mesmo com o dev de teste de pé. Se um falhar ou ficar pendente, o Arquiteto não diz que subiu: avisa qual falhou e pede a decisão.
2. **Pergunta de encerramento imediata.** No mesmo turno em que avisar que instalou nos dois ambientes, o Arquiteto pergunta ao humano se quer encerrar a feature, sem esperar o pedido. A pergunta diz o alcance exato (excluir o Arquiteto, a seção e os grupos, sem volta), o que acontece se confirmar e se negar, com resposta livre. Se a subida falhou ou ficou pendente em algum ambiente, não faz a pergunta: resolve e avisa primeiro (acréscimo do executor).
3. **A pergunta NÃO é autorização.** Continua valendo `arquiteto-destruicao`: só a resposta afirmativa explícita do humano a essa pergunta é o gatilho do aviso ao Bootstrapper; o Arquiteto não exclui nada. Sem resposta, resposta ambígua ou "depois": nenhum handoff e a feature segue aberta. O handoff leva o ponteiro `autorizacao_ref` da resposta (ver `2026-11-20-ponteiro-autorizacao-encerramento.md`); quando a resposta é curta ("sim"), o Bootstrapper confere também a pergunta do Arquiteto e o alcance dela.
4. O gate "produção só com confirmação explícita" continua: a confirmação do humano agora autoriza a subida em dev e prod.

## Fontes alteradas
Skills `arquiteto-review-merge` (seção 13, principal), `arquiteto-destruicao` (seção 24, gatilho), `arquiteto-comunicacao-humana` (seção 4), `arquiteto-regras` (essencial); fichas `markdown\modelos\arquiteto.md` e `fábrica-agêntica-v2.md`; `README.md`; `markdown\fases\fase-review.md` (SUBIDA PARA PRODUÇÃO, itens 4 e 5); diagramas `fase-review` e `fábrica-agentica` (rótulos "BUILD DEV E PROD" e "subir para dev e prod"; sem caixa nova para a pergunta de encerramento: conferir visualmente).
Hashes: tabela em `2026-11-20-ponteiro-autorizacao-encerramento.md` (os dois ajustes foram feitos juntos; os hashes de antes valem para ambos).
