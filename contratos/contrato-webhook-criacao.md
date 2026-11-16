# Contrato — criação de seção e aviso ao Bootstrapper (V2)

## Quem dispara
- O **Bootstrapper** recebe a feature autorizada pelo humano e roda no PC:

```powershell
py -3 "C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\criar-secao-feature.py" "cadastro-fornecedor"
```

- O nome é normalizado (NFC, sem espaços nas pontas, `/` e `\` viram hífen). Nome vazio, com caractere invisível ou reservado é recusado.
- A seção ainda não pode existir. O Grok Bot precisa estar aberto, na área de trabalho desbloqueada.

## O que o script faz
- Hoje o script ainda usa o bot **Âncora V2** para criar a seção: o companion `criar-secao-feature.ps1` move o Âncora V2 para uma seção nova, renomeia a seção, devolve o Âncora V2 à seção Fábrica Agêntica V2 e confere que a seção nova ficou vazia.
- Não cria bot nenhum e não abre sessão do Cursor.
- Devolve `section_id=null`. Só depois de sucesso confirmado (exit 0 e status `CONCLUIDO`) o Bootstrapper busca o ID real da seção (`ListSections`) e cria o Arquiteto nela.

## Saída
- JSON no terminal e em `scripts\logs\criar-secao-<uuid>-final.json`, com `execution_id`, `section_name`, `section_id`, `status`, `exit_code`, `notification` e `needs_human_notification`.
- Exit: 0 sucesso; 2 argumentos inválidos; 3 falha; 124 timeout; 130 interrupção.
- Em falha, conferir o estado antes de repetir: a seção pode ter sido criada pela metade.

## Aviso por webhook (sempre ao terminar)
- **Quando envia:** sempre que o script termina, com sucesso ou com falha (inclusive timeout e interrupção), desde que haja nome de seção válido. Sem nome válido: `not_sent_invalid_section`, sem envio.
- **Quem envia:** `scripts\notificacao_criacao_v2.py`, chamado pelo próprio `criar-secao-feature.py`. O `.ps1` não envia nada.
- **Receptora:** rotina do Bootstrapper **"Fábrica V2 — bloqueio criação"**. Ela só registra o evento e avisa o humano. Não cria, não executa, não corrige e não aciona outro bot.
- **Variáveis:** `FABRICA_V2_CRIACAO_WEBHOOK_URL` e `FABRICA_V2_CRIACAO_WEBHOOK_KEY`. Ainda a configurar pelo humano no PC, a partir da barra lateral do Bootstrapper. Lidas do ambiente do processo ou, se faltarem, das variáveis User do Windows. Chave nunca no código, em argumentos, no chat ou em documentos.
- **Validação:** a URL precisa seguir `https://api2.cursor.sh/automations/webhook/<id>`; fora disso, `invalid_configuration` e nada é enviado. Sem URL ou chave: `not_configured`.
- **Envio:** POST JSON com `Authorization: Bearer <chave>` e `X-Automation-Key: <chave>`. Timeout de 8 s, **uma tentativa, sem retry** e sem redirecionamento. Chave e URL são trocadas por `[redigido]` no texto do erro.

## Payload
| Campo | Valor |
|---|---|
| `execution_id` | texto único da execução |
| `script` | `criar-secao-feature.py` |
| `secao` | nome normalizado da seção |
| `status` | `sucesso` ou `falha` |
| `exit` | número inteiro (0 em sucesso) |
| `erro` | vazio em sucesso; motivo em falha |

## Garantias e limites
- Falha no aviso nunca muda o exit da criação; a lacuna aparece em `notification` e `needs_human_notification`.
- `notification.status`: `not_configured`, `invalid_configuration`, `http_accepted`, `http_rejected`, `send_failed`, `not_sent_invalid_section` ou `notifier_error`.
- **HTTP 200 só prova que o endpoint aceitou**, não que o humano leu: `delivery_confirmed` fica sempre `false`.
- Processo encerrado à força não garante aviso.