# Contrato — destruição de seção e aviso de bloqueio ao Bootstrapper (V2)

## Quem dispara
- O **Arquiteto** roda no PC, só com autorização humana explícita de alvo e escopo, conforme `contratos\contrato-destruicao-api-interna.md`:

```powershell
py -3 "C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\destruir-secao-api.py" --secao-id "<id da seção>" --api-real
```

- Sem `--executar` é só planejamento (dry-run). Execução real e regras de confirmação: ver o contrato de API interna.
- Fim da feature, merge ou aprovação, sozinhos, não autorizam destruir.

## Bot protegido
- **Somente o Bootstrapper** (por ID ou nome exato). Se aparecer no alvo, o script para antes de excluir qualquer coisa.

## Saída
- JSON no terminal e linha no log `scripts\logs\destruir-secao-api.jsonl`, com `status`, `erro`, `stage`, `needs_human_notification`, `motivos_aviso_humano` e, quando houver aviso, `notification`.
- Exit: 0 sucesso ou dry-run; 2 bloqueio; 1 falha.

## Aviso por webhook (só no bloqueio inicial)
- **Quando envia:** só quando o script termina com **exit 2 e `stage=preflight`** (bloqueio na checagem inicial, antes de ler ou excluir qualquer coisa). Uma vez por execução.
- **Demais erros e bloqueios:** nada é enviado. Fica só `needs_human_notification=true` no resultado e no log, e o **Arquiteto repassa** ao humano.
- **Quem envia:** `scripts\notificacao_bootstrapper.py`, chamado pelo `destruir-secao-api.py` antes de imprimir o JSON final. Erro no notificador vira `notification.status=notifier_error` e nunca muda status, erro ou exit.
- **Receptora:** rotina do Bootstrapper **"Fábrica V2 — bloqueio destruição"**. Ela só registra o evento e avisa o humano. Não cria, não executa, não corrige e não aciona outro bot.
- **Variáveis:** `FABRICA_V2_WEBHOOK_URL` e `FABRICA_V2_WEBHOOK_KEY`. Ainda a configurar pelo humano no PC, a partir da barra lateral do Bootstrapper. Lidas do ambiente do processo ou, se faltarem, das variáveis User do Windows. Chave nunca no código, em argumentos, no chat ou em log.
- **Validação:** a URL precisa seguir `https://api2.cursor.sh/automations/webhook/<id>`; fora disso, `invalid_configuration` e nada é enviado. Sem URL ou chave: `not_configured`.
- **Envio:** POST JSON com `Authorization: Bearer <chave>` e `X-Automation-Key: <chave>`. Timeout de 8 s, **uma tentativa, sem retry** e sem redirecionamento. Chave e URL são trocadas por `[redigido]` no texto enviado.

## Payload
| Campo | Valor |
|---|---|
| `execution_id` | ID da execução (o mesmo do log) |
| `script` | `destruir-secao-api.py` |
| `feature` | nome da seção, se já conhecido (no bloqueio inicial costuma vir vazio) |
| `exit` | `2` |
| `erro` | texto do campo `erro` do resultado |
| `motivos_aviso_humano` | lista do resultado |
| `status` | `aguardando_humano` |

## Garantias e limites
- `notification.status`: `not_configured`, `invalid_configuration`, `http_accepted`, `http_rejected`, `send_failed` ou `notifier_error`.
- **HTTP 200 só prova que o endpoint aceitou**, não que o humano leu: `delivery_confirmed` fica sempre `false`.
- O aviso não autoriza nova tentativa de exclusão. Rodar de novo é outra execução, não retry do aviso.