# Decisão: Âncora V2 entra no lugar do Âncora antigo na lista de fixos do cliente da API

**Data:** 15/11/2026, por volta das 22h12 (horário da Bahia)
**Decisão de:** Elienaldo, por voz
**Executado por:** Mestre de obras

## O que foi decidido
Em `FIXOS_POR_ID`, no arquivo `scripts/grokbot_api_client.py`, troquei o Âncora antigo (`9b3c5289-8ed7-4805-88d5-bc536ec4e40d`) pelo Âncora V2 (`3aa31f55-37e8-46e5-a430-a20b42844084`), o bot que acabou de ser renomeado no app.

## Por quê
A lista deve ter só os bots da V2, como nas decisões anteriores do mesmo dia. O ID antigo não é o Âncora V2.

## Efeito
O cliente da API da V2 passa a recusar `delete_agent` e `delete_room` para o Âncora V2 e deixa de recusar para o Âncora antigo.

## O que mudou
- Só essa linha. O resto do arquivo não foi alterado.
- Hash SHA-256: `13EBBC1B…` antes, `05EC3167…` depois.
- O backup está em `Fabrica-Agentica-backups\api-client-ancora-v2-fixo-20261115-2212`.
- Conferência depois de salvar: a comparação com o backup mostra só essa linha, e o módulo importado lista Âncora V2, Mestre de obras e Bootstrapper.
- Não houve commit.
- Decisões anteriores relacionadas: `2026-11-15-bootstrapper-fixo-api-client.md` e `2026-11-15-fixos-api-client-sem-v1.md`.