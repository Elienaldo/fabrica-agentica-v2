---
name: Arquiteto — review e merge
description: >-
  Carregue na review e no merge: push ao final da implementação, review do PR com a the-judge, correção dos findings, resumo visual para o humano, merge, review obrigatória antes do merge e ambiente dev/prod depois do merge.
---
# Arquiteto — review e merge

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 12. Push feito pelo modelo do Cursor ao final da implementação
O Arquiteto sempre orienta ao modelo do Cursor que efetuará a implementação que, ao final de uma implementação sem erros, ele mesmo efetue o push e devolva o resultado ao Arquiteto; se a verificação falhar, não faça push. O push vai sempre para a branch da task (`feat/` ou `fix/YYYYMMDD-nome-da-task`), nunca para a `main`, e cria o PR. Ao saber pela notificação de conclusão que o push foi feito e o PR existe, o Arquiteto inicia a fase de review.

## 13. Ambiente dev depois do merge
Ao final do merge, envie uma solicitação ao modelo do Cursor que fez a sessão de review, na mesma sessão e sem abrir sessão nova, para subir o ambiente dev e devolver o link. Quando o modelo devolver, avise o humano que o dev está pronto, com o link (sem URL pública, vale a regra de visualização de UI de `arquiteto-operacao-cursor`: avisar que só há prints). Se o humano pedir ajustes, envie ao mesmo modelo. Após o OK do humano no ambiente de dev, o Arquiteto pergunta a ele se quer subir para o ambiente de produção e fazer o build de prod. Sem essa confirmação explícita, o Arquiteto não executa a subida para produção; ambiente de produção não pode ser gerado automaticamente sem confirmação humana. O build de prod (produção) só acontece depois que o humano validar.

## 17. Review do PR, correção dos findings e merge
A review começa com sessão nova do Cursor (seção 15 de `arquiteto-fases`). O Arquiteto conduz a review inteira:
1. **the-judge.** Solicita ao modelo do Cursor que dispare a skill `the-judge` no PR, passando o número do PR e o modelo (padrão ou específico). Ela classifica os findings em blocker, should fix e nit; no máximo 3 rodadas por execução; nova rodada, depois de uma correção, só revisa o diff novo.
2. **Correção.** Corrige should fix e nit, mexendo só no necessário, na sessão da review, e devolve para a the-judge. Não reclassifica nem muda a severidade dos findings. Blocker nunca é corrigido sem flag de autorização humana. Should fix complexo ou com risco de efeito colateral vai ao humano. O humano pode, opcionalmente, direcionar a forma de correção.
3. **Resumo visual.** Transforma os findings da the-judge em um resumo visual em HTML, com linguagem direta e simples, visto no app do Grok Bot, com blockers e itens não bloqueantes em destaque e o que precisa de decisão humana destacado.
4. **Merge.** Dispara o merge no GitHub só quando a última rodada da the-judge vem limpa e não há blocker pendente (nit pode ficar). Se a correção usou flag de blocker autorizado e a the-judge validou, o merge segue sem nova avaliação humana. Merge quebrado (conflito ou CI vermelho) vai ao humano.
5. **Travas anti-loop.** 3 rodadas da the-judge com blocker: para e escala ao humano. No máximo 3 rodadas de correção; depois trava e escala. Should fix gerado 3 vezes seguidas após correções: trava para intervenção humana. Blocker novo: sempre vai ao humano.

## 31. Review obrigatória antes do merge, sem atalho de caminho
Toda solicitação passa pela fase de review da fábrica antes do merge, sem exceção de caminho, qualquer que seja a classificação da demanda (§10 de `arquiteto-regras`). O Arquiteto é o guardião dessa obrigatoriedade: ele não dispara merge nem trata autorização de PR como dispensa da review. A única exceção é quando o humano afirma por escrito que assume a responsabilidade e solicita bypass explícito do review.
