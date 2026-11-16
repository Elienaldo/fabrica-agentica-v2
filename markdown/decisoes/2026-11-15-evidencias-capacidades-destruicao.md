# Registro: evidências das capacidades de destruição pela API interna

**Data:** 15/11/2026, por volta das 22h40 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que este registro diz
As capacidades da rota de API interna usadas por `scripts/destruir-secao-api.py` foram validadas em testes reais, com bots, seção e grupo descartáveis:

| Capacidade | Teste | Data | Resultado registrado |
|---|---|---|---|
| bloco `api_interna` (leitura de inventário e rota) | Stage A + Stage B | 12/11/2026 | validado |
| `bot_delete` | Stage B: `DeleteGrokBotAgent {id: agentId}` em dois bots descartáveis | 12/11/2026 | HTTP 200 nas duas chamadas |
| `section_delete` | Stage B: `UpdateGrokBotUserRuntimeSettings` com a lista inteira sem a seção descartável, por `destruir-secao-api.py --api-real` | 12/11/2026 | HTTP 200; seções reais idênticas ao backup |
| `room_delete` | Stage 6: `DeleteGrokBotAgent {id: roomId}` em grupo descartável | 13/11/2026, 19h39 (horário da Bahia) | HTTP 200; o grupo sumiu e os demais 18 agentes ficaram intactos |

**Fonte:** os campos `validation_evidence` de `scripts/destruir-secao-config.json` antes desta mudança (versão no commit `f3516b6` e no backup `Fabrica-Agentica-backups\config-evidencia-v2-20261115-2240`). Esses testes foram feitos antes da separação da V2, com ferramentas e pastas de diagnóstico da fábrica anterior.

## Evidência bruta
Por decisão do Elienaldo, a evidência bruta (relatórios e JSONs dos diagnósticos) fica fora da V2. Os campos `validation_evidence` do config passaram a apontar para este registro, sem caminhos da V1.

## O que mudou no config
- Os 4 campos `validation_evidence` do bloco `api_interna` (bloco, `bot_delete`, `section_delete` e `room_delete`) agora trazem um resumo do teste e o ponteiro para este registro.
- Nenhum `validated` mudou. O script só exige `validated: true` e `validation_evidence` não vazio (`destruir-secao-api.py`, linha 117). Ele não valida formato nem existência de caminho, então as capacidades continuam liberadas.
- `scripts/destruir-secao-config.json`: hash SHA-256 `FFDE6824` → `99464B45`. Mantém UTF-8 sem BOM e LF, e o JSON continua válido.
- Backup: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\config-evidencia-v2-20261115-2240`.

## Conferência
- `liberacao_api_interna()` devolve `(True, '')` para o bloco e para `bot_delete`, `section_delete` e `room_delete`. Rodei só a função de leitura do config, sem dry-run e sem nenhuma chamada real.
- Testes puros: 69 testes OK (13 de `test_notificacao_criacao_v2`, 13 de `test_notificacao_bootstrapper` e 43 de `test_destruir_secao_api`). Não sobrou `__pycache__`.
- Nenhum `validation_evidence` cita mais `diagnostico-*`, `stageA/B/6-*` ou `RELATORIO`.

## Ainda com referências da fábrica anterior (não alterado)
- `observation_evidence` do bloco `api_interna` (linha 53) cita `diagnostico-apiinterna-stageA-1112/...`.
- Os campos da rota de tela, aposentada (linhas 18, 30 e 42), citam diagnósticos `t1089`, `t1111` e `t924`.
- A `nota` de `room_delete` (linha 69) cita `stage6_teste_room_delete.py`.
- O script não lê nenhum desses campos para liberar capacidades. Limpar fica para decisão do humano.

## Commit
Não houve commit.
