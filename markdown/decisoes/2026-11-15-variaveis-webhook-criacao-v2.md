# Decisão: variáveis do webhook de bloqueio na criação da V2

**Data:** 15/11/2026, por volta das 22h20 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi configurado
Duas variáveis de ambiente do usuário no Windows do PC-ELIENALDO (`HKCU\Environment`), que o `scripts/notificacao_criacao_v2.py` usa para avisar a rotina "Fábrica V2 — bloqueio criação" do Bootstrapper:
- `FABRICA_V2_CRIACAO_WEBHOOK_URL`: o Elienaldo colou a URL no chat. Ela não existia antes.
- `FABRICA_V2_CRIACAO_WEBHOOK_KEY`: o Elienaldo preencheu num campo protegido. O valor passou por um arquivo temporário, que foi apagado em seguida, e não aparece em nenhum log nem neste documento. A variável não existia antes.

## Verificação
- Reli a variável depois de gravar: 69 caracteres. O SHA-256 do valor gravado (8 primeiros caracteres, `FB3AD715`) é igual ao do valor recebido.
- Backup do registro antes da mudança em `Fabrica-Agentica-backups\env-fabrica-v2-criacao-key-20261115-2220`. O export de `HKCU\Environment` tinha hash `35C2392E` antes e `8F223358` depois. Atenção: o backup contém valores sensíveis, então não deve ser compartilhado.
- As variáveis da V1 não foram alteradas.

## Pendente
`FABRICA_V2_WEBHOOK_URL` e `FABRICA_V2_WEBHOOK_KEY`, que são da rotina "Fábrica V2 — bloqueio destruição".

Não houve commit.
## Atualização 22h21
- `FABRICA_V2_WEBHOOK_URL` (rotina bloqueio destruição): URL colada pelo Elienaldo, não existia antes, gravada e relida. Falta só `FABRICA_V2_WEBHOOK_KEY`.

## Atualização das 22h22
- `FABRICA_V2_WEBHOOK_KEY` (rotina de bloqueio na destruição): o Elienaldo preencheu o valor num campo protegido. Ela não existia antes. Foi gravada e relida: 69 caracteres, e o SHA-256 bate com o recebido (`88A97A56`). O arquivo temporário foi apagado.
- Backup do registro em `Fabrica-Agentica-backups\env-fabrica-v2-destruicao-key-20261115-2221`: export `39E6FAFD` antes e `3C882D47` depois.
- As quatro variáveis `FABRICA_V2_*` estão configuradas. Os scripts só enxergam essas variáveis em terminais abertos depois desta gravação.
