---
name: Arquiteto — log de tokens
description: >-
  Carregue para registrar o log de tokens por chamada ao modelo em logs\consumo-tokens.jsonl da V2 (append-only).
---
# Arquiteto — log de tokens

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 29. Log de tokens
Em toda conversa, registrar uma linha no log por chamada ao modelo, só com o que o próprio bot consegue extrair da chamada: nome do bot, identificador da conversa, timestamp, fase, feature, modelo usado e handoff que originou a chamada. Se a API devolver dados de tokens no retorno da chamada, registrar também esses números; se não devolver, não incluir campos de tokens (nunca inventar valores). Sem esse registro, a chamada não fecha.
Destino único: `logs\consumo-tokens.jsonl` na raiz da V2 (`C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\logs\`), append-only, uma linha por evento. Campos do evento: bot, conversa, timestamp, fase, feature, modelo, handoff (handoff que originou a chamada); os campos de tokens só entram quando a API os devolver.
