# Registro: URLs de webhook no histórico do git da V2

**Data:** 15/11/2026, por volta das 22h45 (horário da Bahia)
**Pedido de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi encontrado
- O histórico do repositório (`git log --all -p`) tem **2 URLs completas** de webhook (`api2.cursor.sh/automations/webhook/<uuid>`), uma em cada contrato:
  - `contratos/contrato-webhook-criacao.md` (SHA-256 da URL: `CC7ACC2F…`);
  - `contratos/contrato-webhook-destruicao.md` (SHA-256 da URL: `C94FEFE0…`).
- As duas entraram no commit `ddab017` (13/11/2026), continuaram em `522460f` e foram removidas do arquivo em `f3516b6` (15/11/2026). Continuam nos commits anteriores, que já estão no remoto `origin`.
- Não há outras URLs de webhook no histórico inteiro. Também não apareceu chave com valor, Bearer nem token no histórico.
- Nenhum arquivo rastreado hoje contém URL real de webhook.
- Os valores não foram impressos nem gravados em arquivo. A comparação foi feita na memória, só por igualdade, e os hashes acima são da própria URL.

## Comparação com as variáveis de usuário (só igual ou diferente)
| URL do histórico | `FABRICA_V2_CRIACAO_WEBHOOK_URL` | `FABRICA_V2_WEBHOOK_URL` |
|---|---|---|
| `CC7ACC2F…` (contrato de criação) | diferente | diferente |
| `C94FEFE0…` (contrato de destruição) | diferente | diferente |

Comparei também, só para leitura e sem alterar nada, com as variáveis da fábrica anterior. As duas URLs do histórico são iguais às de `FABRICA_CRIACAO_WEBHOOK_URL` e `FABRICA_SUPERVISOR_WEBHOOK_URL`, uma para cada. Ou seja: o que está exposto no histórico são os webhooks das rotinas da fábrica anterior, não os da V2.

## Situação
- O código da V2 lê as URLs e as chaves das variáveis de ambiente (`notificacao_criacao_v2.py` e `notificacao_bootstrapper.py`) e não tem URL embutida. Nada foi alterado no código.
- O histórico remoto não foi reescrito.
- **Nenhum webhook foi rotacionado.**

## Pendência
- Webhooks da V2: não aparecem no histórico, então não precisam de rotação por esse motivo.
- Webhooks da fábrica anterior (rotinas de criação e de bloqueio na destruição do Supervisor): as URLs estão expostas no histórico da V2. Se o humano quiser invalidar essas URLs, é preciso regenerar o webhook e a chave nas rotinas correspondentes no Cursor e atualizar as variáveis `FABRICA_CRIACAO_WEBHOOK_*` e `FABRICA_SUPERVISOR_WEBHOOK_*`. Isso fica fora da V2 e não pode ser feito por script. Fica para decisão do humano.

## Commit
Não houve commit.
