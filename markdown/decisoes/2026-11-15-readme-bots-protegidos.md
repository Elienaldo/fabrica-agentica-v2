# Decisão: corrigir no README os bots protegidos

**Data:** 15/11/2026, por volta das 22h35 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi decidido
Corrigir a frase "Único bot protegido: o Bootstrapper" na seção 5 do `README.md` usando o que está de fato em `scripts/grokbot_api_client.py`.

## O que está no código (conferido em 15/11/2026)
- `FIXOS_POR_ID` em `grokbot_api_client.py` (linhas 45 a 49): `3aa31f55-37e8-46e5-a430-a20b42844084` (Ancora V2), `c48d6f40-b5af-48ce-8a00-da7561b3a82a` (Mestre de obras) e `f99cfa31-bd1e-4687-a134-e31c3e7444f9` (Bootstrapper).
- `destruir-secao-api.py` (linhas 40 e 74): no plano, o script bloqueia só o Bootstrapper como bot protegido. A frase do README também cita isso, para não esconder a diferença.

## O que mudou
- `README.md`, seção 5: "Único bot protegido: o **Bootstrapper**." virou "Bots protegidos: o cliente da API (`FIXOS_POR_ID` em `scripts/grokbot_api_client.py`) recusa excluir três: Âncora V2 (`3aa31f55…`), Mestre de obras (`c48d6f40…`) e Bootstrapper (`f99cfa31…`); o script de destruição, no plano, bloqueia o Bootstrapper." O resto da linha, com as seções protegidas, não mudou.
- Hash SHA-256: `B304CA2E` → `C9F1D65C`.
- Backup: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\readme-bots-protegidos-20261115-2235`.
- Releitura: a comparação com o backup mostra só essa linha.

## Commit
Não houve commit.
