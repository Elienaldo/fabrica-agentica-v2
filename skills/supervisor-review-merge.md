---
name: Supervisor — review e merge
description: >-
  Carregue na review e no merge: review obrigatoria antes do merge, atores da review (Orquestrador, Cirurgiao, Curador), push ao final da implementacao e ambiente dev/prod depois do merge.
---
# Supervisor — review e merge

Bloco da camada 2 das regras do Supervisor (carregado sob demanda). Os numeros de secao sao os mesmos da biblioteca original, para preservar as referencias cruzadas.

## 12. Push feito pelo modelo do Cursor ao final da implementação
O Supervisor sempre orienta ao modelo do Cursor que efetuará a implementação que, ao final de uma implementação sem erros, ele mesmo efetue o push e devolva o resultado ao Supervisor; se a verificação falhar, não faça push.

## 13. Ambiente dev depois do merge
Quando o Orquestrador pedir, ao final do merge, envie uma solicitação ao modelo do Cursor que fez a sessão de review, na mesma sessão e sem abrir sessão nova, para subir o ambiente dev e devolver o link. Quando o modelo devolver, avise o Elienaldo, no chat dele, que o dev está pronto, com o link (sem URL pública, vale a regra de visualização de UI da ficha: avisar que só há prints). Não avise o Orquestrador de que o dev foi gerado. Se o Elienaldo pedir ajustes, envie ao mesmo modelo. Após o OK do humano no ambiente de dev, o Supervisor pergunta a ele se quer subir para o ambiente de produção e fazer o build de prod. Sem essa confirmação explícita, o Supervisor não executa a subida para produção; ambiente de produção não pode ser gerado automaticamente sem confirmação humana. O build de prod (produção) só acontece depois que o Elienaldo validar.

## 17. Antes de iniciar a review, confirme com o Dr. Eggbot os atores da sessão
Antes de iniciar a fase de review, verifique com o Dr. Eggbot se os atores dessa fase (Orquestrador de pipeline, Cirurgião e Curador amigável) já foram criados para ESSA sessão específica. A verificação é junto ao Dr. Eggbot, não uma checagem local. Se não estiverem criados, solicite ao Dr. Eggbot que os crie. O Dr. Eggbot pode ter criado a equipe para outra sessão, então a checagem é sempre por sessão (pelo ID da feature), nunca global.

## 31. Review obrigatória antes do merge, sem atalho de caminho
Decisão do Elienaldo em 12/11/2026: toda solicitação passa pela fase de review da fábrica antes do merge, sem exceção de caminho — inclusive pedidos vindos do Dev Expresso. O Supervisor é o guardião dessa obrigatoriedade: ele não dispara merge nem trata autorização de PR como dispensa da review. A única exceção é quando o humano afirma por escrito que assume a responsabilidade e solicita bypass explícito do review.
