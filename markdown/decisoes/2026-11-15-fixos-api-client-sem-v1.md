# Decisão: remover os bots da V1 da lista de fixos do cliente da API

**Data:** 15/11/2026, por volta das 22h06 (horário da Bahia)
**Decisão de:** Elienaldo, por voz
**Executado por:** Mestre de obras

## O que foi decidido
Tirar de `FIXOS_POR_ID`, em `scripts/grokbot_api_client.py`, os três bots da V1: Supervisor (`bb806181…`), Dev Expresso (`0a378d5e…`) e dr eggbot (`f8013422…`). Ficam na lista só Ancora (`9b3c5289…`), Mestre de obras (`c48d6f40…`) e Bootstrapper (`f99cfa31…`).

## Por quê
A V2 é separada da V1, então a lista de bots protegidos da V2 só deve ter bots que fazem parte dela.

## Efeito
O cliente da API da V2 deixa de recusar `delete_agent` e `delete_room` para os três IDs removidos.

## O que mudou
- Saíram só essas três linhas. O resto do arquivo não foi alterado.
- Hash SHA-256: `39EF403B…` antes e `13EBBC1B…` depois.
- O backup está em `Fabrica-Agentica-backups\api-client-fixos-sem-v1-20261115-2206`.
- Conferência depois de salvar: a comparação com o backup mostra só essas três linhas removidas, e o módulo importado tem 3 IDs na lista.
- Não houve commit.
- Decisão anterior relacionada: `2026-11-15-bootstrapper-fixo-api-client.md`.