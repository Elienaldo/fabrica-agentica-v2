# Decisão: remover a regra 32 (exclusão dos cards de execução) da V2

**Data:** 17/11/2026, por volta das 16h40 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi decidido
Remover a regra 32 ("Exclusão dos cards de execução ao encerrar um pedido") só da Fábrica Agêntica V2. A V1 e o `GrokBot-Scripts` não foram tocados.

## Motivo
A regra nasceu na V1, para os cards que o Supervisor criava no desktop do Grok. Na V2 ela ficou ambígua e levou à exclusão das sessões do Cursor ao encerrar uma feature. Como o Arquiteto da V2 é excluído ao final da feature, a regra não é mais necessária.

## O que mudou
- `skills\arquiteto-destruicao.md`: removida a seção 32 inteira e, na descrição, o trecho "ou para excluir os cards de execução de um pedido já encerrado pelo humano".
- `skills\arquiteto-regras.md`: o gatilho "destruir seção/bots/grupos da feature ou excluir cards de execução" passou a "destruir seção/bots/grupos da feature", e o índice passou de "§24, §32" para "§24".
- `markdown\modelos\arquiteto.md`, item 7: tirada a parte "ou exclui os cards de execução de um pedido encerrado".
- `contratos\contrato-destruicao-api-interna.md`: removida a seção "Cards de execução" (a frase da regra 32 e a linha seguinte, que dependia dela).
- Nenhuma outra seção foi renumerada. A seção 24 segue igual.

## Arquivos e hashes (SHA-256, 8 primeiros caracteres)
- `skills\arquiteto-destruicao.md`: `1E94BB31` antes, `F568146D` depois.
- `skills\arquiteto-regras.md`: `33C4C3A3` antes, `A4FEA7A8` depois.
- `markdown\modelos\arquiteto.md`: `08CD7CC3` antes, `89024DEB` depois.
- `contratos\contrato-destruicao-api-interna.md`: `7966601C` antes, `A2EEDEAA` depois.
- Backup no PC: `Fabrica-Agentica-backups\remover-regra32-v2-20261117-1637` (arquivos do PC em `pc`, cópias da biblioteca do box em `box`).

## Pendências
- A biblioteca do box (`arquiteto-destruicao` e `arquiteto-regras`) ainda precisa receber o conteúdo preparado em `/workspace/staging-regra32`; o box e o espelho do PC eram idênticos antes e devem voltar a ser.
- O nome e o título da skill `arquiteto-destruicao` ainda dizem "destruição e exclusão de cards"; não foram alterados para não renomear a skill.
- Sem commit.