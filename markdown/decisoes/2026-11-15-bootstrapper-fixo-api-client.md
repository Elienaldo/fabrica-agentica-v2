# Decisão — Bootstrapper na lista de bots fixos do cliente da API

**Data:** 15/11/2026, 22h05 (horário da Bahia)
**Decisão de:** Elienaldo (por voz)
**Executado por:** Mestre de obras

## O que foi decidido
Acrescentar o Bootstrapper (`f99cfa31-bd1e-4687-a134-e31c3e7444f9`) à lista `FIXOS_POR_ID` de `scripts/grokbot_api_client.py`, no mesmo padrão dos outros bots fixos.

## Por quê
O Bootstrapper é o bot de entrada da V2 e o único bot protegido. Até agora a proteção dele estava só no script de destruição. Com esta mudança, o cliente também passa a recusar `delete_agent` e `delete_room` para esse ID, o que cria uma segunda barreira.

## O que mudou
- Foi acrescentada só uma linha: `"f99cfa31-bd1e-4687-a134-e31c3e7444f9",  # Bootstrapper`.
- Nada mais foi alterado no arquivo. Os outros IDs continuam como estavam, e o "via Supervisor" da linha 5 também.
- Hash SHA-256 antes: `569B95E5…`. Hash depois: `39EF403B…`.
- Backup em `Fabrica-Agentica-backups\api-client-bootstrapper-fixo-20261115-2205`.
- Conferido depois de salvar: o diff contra o backup mostra só essa linha, a sintaxe Python está OK e, ao importar o módulo, o ID aparece na lista (6 itens).
- Sem commit.