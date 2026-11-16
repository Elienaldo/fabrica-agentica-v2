# Decisão: tirar resultado.json da skill arquiteto-destruicao

**Data:** 15/11/2026, por volta das 22h15 (horário da Bahia)
**Decisão de:** Elienaldo, por voz
**Executado por:** Mestre de obras

## O que foi decidido
Alinhar as linhas 23 a 25 da skill `arquiteto-destruicao` com o que o script faz hoje. `destruir-secao-api.py` não grava `log_dir/resultado.json`: ele devolve o JSON no stdout e registra em `destruir-secao-api.jsonl`.

## O que mudou (só na linha 23)
- Onde dizia "log_dir/resultado.json", agora diz "o log JSONL `destruir-secao-api.jsonl` (o script não grava arquivo de resultado à parte)".
- Onde dizia que o script "não envia aviso por conta própria", agora diz "Fora o aviso automático de bloqueio no preflight (item 6), ..." Motivo: na V2, o script manda sozinho o aviso de bloqueio do preflight (exit 2) para a rotina do Bootstrapper, por `notificacao_bootstrapper.py`.
- O resto continua igual: o script devolve `needs_human_notification` com o motivo, o hook cobre só preflight com exit 2 (linha 24), e sem casamento único o Arquiteto mantém o bloqueio e avisa o humano (linha 25).
- As linhas 24 e 25 não mudaram de texto. As linhas 22 e 26 e o restante do arquivo ficaram intactos (conferido por diff).

## Arquivos e hashes (SHA-256, 8 primeiros caracteres)
- Cópia em `/home/box/agent-data/workflows/arquiteto-destruicao/SKILL.md`: `0480821E` antes, `0591B2F9` depois.
- Cópia em `skills\arquiteto-destruicao.md`, na V2: `0480821E` antes, `0591B2F9` depois.
- Backups: no box, em `/workspace/backups/arquiteto-destruicao-sem-resultado-json-20261115-2215`; no PC, em `Fabrica-Agentica-backups\arquiteto-destruicao-sem-resultado-json-20261115-2216`.
- A descrição no app não precisou ser atualizada, porque o bot Arquiteto ainda não foi criado.
- Não houve commit.