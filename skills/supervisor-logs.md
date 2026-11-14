---
name: Supervisor — log de tokens
description: >-
  Carregue para registrar o log de tokens por chamada ao modelo em logs/consumo-tokens.jsonl (append-only).
---
# Supervisor — log de tokens

Bloco da camada 2 das regras do Supervisor (carregado sob demanda). Os numeros de secao sao os mesmos da biblioteca original, para preservar as referencias cruzadas.

## 29. Log de tokens (11/11/2026)
Em toda conversa, registrar uma linha no log por chamada ao modelo, só com o que o próprio bot consegue extrair da chamada: nome do bot, identificador da conversa, timestamp, fase, feature, modelo usado e handoff que originou a chamada. Se a API devolver dados de tokens no retorno da chamada, registrar também esses números; se não devolver, não incluir campos de tokens (nunca inventar valores). Sem esse registro, a chamada não fecha.
Destino único: `logs/consumo-tokens.jsonl` na raiz da Fábrica (C:\Users\Elienaldo\Projetos\Fabrica-Agentica\logs\), append-only, uma linha por evento. Campos do evento: bot, conversa, timestamp, fase, feature, modelo, handoff (handoff que originou a chamada); os campos de tokens só entram quando a API os devolver.
