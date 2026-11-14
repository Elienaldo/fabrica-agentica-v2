# Cruzamento de consumo de tokens — 8/11 vs 12/11 de 2026

## O que são estas páginas
Dois painéis HTML, mesmo layout, métricas e seções, feitos a partir do CSV de uso do Cursor, recortados por dia em America/Bahia (UTC-3):

- `dashboard-consumo-08-11.html` — dia 8 de novembro de 2026 (dia completo, 00h00:01 às 20h42:15).
- `dashboard-consumo-12-11.html` — dia 12 de novembro de 2026 (recorte PARCIAL: 01h00:28 às 17h26:58, o dia ainda estava em andamento quando o CSV foi exportado).

## Para que serve o cruzamento
Comparar as duas datas e verificar se houve redução do consumo de tokens depois dos ajustes feitos na Fábrica Agêntica. As duas páginas usam exatamente a mesma estrutura (Conclusão, KPIs, Ranking por produto e modelo, Tokens por hora, "O que este painel não mede", rodapé) e as mesmas definições (Total = prompt + cache lido + cache escrito + saída; Sem cache = prompt + saída), para que os números fiquem lado a lado.

## Números-chave
| Métrica | 8/11 (completo) | 12/11 (parcial até 17h06) |
|---|---|---|
| Total do dia | 356.457.528 | 118.582.522 |
| Cache lido (%) | 93,9% | 93,8% |
| Sem cache | 9.395.897 | 3.422.413 |
| Eventos | 2.917 | 1.137 |
| Pico horário | 02h–03h (64.436.764) | 11h–12h (35.652.193) |

## Ressalva importante (não inventar comparação cheia)
O recorte do dia 12 é PARCIAL (termina às 17h26:58). O número total do dia 12 vai subir conforme o dia avança, então a comparação direta de totais do dia inteiro ainda não é justa. O que já dá para ler com segurança:
- O peso do cache relido continua praticamente igual (93,9% → 93,8%): o gargalo segue sendo contexto relido.
- No produto `cursor`, o dia 8 foi dominado por `grok-4.7-high-fast` e o dia 12 aparece sobretudo como `grok-4.7-high`.

Para um cruzamento de dia inteiro, reexportar o CSV depois do fim do dia 12 e regerar `dashboard-consumo-12-11.html`.

## Cruzamento com o log dos bots (12/11)
Fonte: `logs\consumo-tokens.jsonl`, gerado hoje pela Fábrica. 10 registros, 11h30 a 14h35 (America/Bahia), todos do bot **Supervisor**, feature `compras-lista-valor-parcela-quantidade`, modelo grok-4.7 high (`context=500k` nos últimos), fases fix → preview → review → pr-merge → prod. São registros de **handoff** (bot, fase, feature, agente do Cursor), não de contagem de tokens.

**Confirma o CSV:** a janela do log (11h30–14h35) cai exatamente no pico do CSV (11h–13h). O produto `cursor / grok-4.7-high` do CSV (16.931.978 tokens, 14,3% do dia) casa com os 8 agentes em nuvem (`bc-…`) que o Supervisor disparou nesse ciclo.

**Diverge / não cobre:**
- O log não tem números de tokens — cruza horário e autoria, não valor absoluto. Reconciliação de tokens só pelo CSV.
- O log só registra o Supervisor. Os 78,8% de `grok-bot` (chat dos próprios bots) não aparecem no log.
- O log termina às 14h35; o CSV vai até 17h26 — consumo das 15h/16h/17h sem registro no log.

**Conclusão do cruzamento:** o log e o CSV se confirmam no que coincidem (ciclo do Supervisor na feature de compras, no pico da tarde), mas o log é parcial: não mede tokens e não cobre o chat dos bots nem o fim do dia. Para medição de consumo por bot/fase em tokens, ainda depende do CSV do Cursor.

## Link compartilhável (Canvas)
Página publicada como Canvas (link clicável, mesma auditoria do dia 12 com o cruzamento): https://cursor.com/canvas/store-cd3ab03d-ef33-48b9-85a4-d796d059d2e0/c8f5e7f6-58f5-495d-96fa-6a7c49969aaf

## Como foi gerada
Fonte: CSV de uso do Cursor enviado pelo Elienaldo em 12/11/2026 (colunas Event Time, Product, Model, Usage JSON). Horários UTC convertidos para America/Bahia. Script de geração espelha o layout do painel do dia 8. Nenhum valor foi inventado; métricas sem dado são sinalizadas na própria página.
