# Decisão: o handoff do Arquiteto dispensa a reconfirmação do humano no encerramento

**Data:** 17/11/2026, ~17:59 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras
**Substitui:** o passo 4 de `2026-11-17-encerramento-feature-bootstrapper.md` (o Bootstrapper confirma direto com o humano). O restante daquela decisão continua valendo.

## O que foi decidido
Quando o Bootstrapper recebe o handoff de encerramento do Arquiteto, o humano já autorizou. O Bootstrapper executa o encerramento (Arquiteto, depois a seção, depois os grupos) sem pedir a confirmação humana de novo. Antes valia "autorização repassada por bot não vale"; isso muda só para o handoff do próprio Arquiteto da seção, e só se passar nas travas abaixo.

## Travas que ficam
- **(a) Remetente e seção.** O handoff precisa vir do próprio Arquiteto da seção: o remetente é o bot cujo id é igual a `arquiteto_id`, e esse bot está dentro de `secao_id` (confirmado por `ListSections`). O handoff traz `autorizacao_texto` e `autorizacao_hora`.
- **(b) Dry-run.** O dry-run continua obrigatório antes de `--api-real --executar`.
- **(c) Divergência.** Se houver divergência, o Bootstrapper PARA e pergunta ao humano. Divergência é: remetente diferente de `arquiteto_id`; seção que não bate; alvo protegido; alvo além do Arquiteto e dos grupos informados; grupos do dry-run diferentes dos do handoff; `needs_human_notification` verdadeiro; ou qualquer campo faltando.
- **(d) Ordem e grupos.** A ordem continua Arquiteto, seção e grupos. `--confirmar-grupos` só leva os ids exatos do handoff que batem com o dry-run.

## O que NÃO muda
Um pedido de encerramento que não venha do handoff do Arquiteto continua exigindo a confirmação direta do humano ao Bootstrapper (alvo e alcance). Exemplos: veio de outro bot, ou o humano pediu fora do fluxo. A autorização repassada por qualquer outro bot não vale. O Arquiteto continua sem excluir nada, e o Bootstrapper continua protegido (nunca é alvo). O script `destruir-secao-api.py` não mudou de comportamento: só o docstring.

## O que mudou
- Skills (biblioteca carregável e espelho no PC): `bootstrapper-encerramento` (seções 1 a 5; descrição ajustada), `bootstrapper-start`, `bootstrapper-criacao-arquiteto`, `arquiteto-destruicao` e `arquiteto-regras`.
- Fichas: `markdown\modelos\bootstrapper.md`, `arquiteto.md` e `fábrica-agêntica-v2.md` (texto, diagrama mermaid e tabela de gates).
- Contratos: `contrato-destruicao-api-interna.md` (travas), `contrato-webhook-destruicao.md` e `fluxo-contrato-verificacao.md`.
- Documentos: `README.md` e `markdown\comunicacao.md`; nota de atualização em `2026-11-17-encerramento-feature-bootstrapper.md`.
- Script: só o docstring de `scripts\destruir-secao-api.py`.
- Diagramas (só o texto dos elementos afetados, JSON válido): `destruicao-api-interna`, `gerenciamento-secoes-por-feature`, `fábrica-agentica`, `acompanhamento\acompanhamento-comunicacao`, `contrato\fluxo-contrato-verificacao`, `review\fase-review`, `fabrica-agentica-visao-geral` e `fabrica-agentica-visao-geral-v2`.
- Não alterados: `checklist-v2.html` (histórico) e as decisões antigas de 15/11.

## Arquivos e hashes (SHA-256, 8 primeiros caracteres)
| Arquivo (V2) | Antes | Depois |
|---|---|---|
| `contratos\contrato-destruicao-api-interna.md` | `3E754B87` | `42070AD0` |
| `contratos\contrato-webhook-destruicao.md` | `D1AE66E3` | `122AF579` |
| `contratos\execucao-verificacao\fluxo-contrato-verificacao.md` | `2B0EDEED` | `F3AE0CC0` |
| `excalidraw\acompanhamento\acompanhamento-comunicacao.excalidraw` | `7054798E` | `65CE0F71` |
| `excalidraw\contrato\fluxo-contrato-verificacao.excalidraw` | `28BC71CC` | `28510080` |
| `excalidraw\destruicao-api-interna.excalidraw` | `188660FC` | `26E190BF` |
| `excalidraw\fábrica-agentica.excalidraw` | `4E9AAE3D` | `02ED0D4D` |
| `excalidraw\fabrica-agentica-visao-geral.excalidraw` | `5BA48254` | `EFED1442` |
| `excalidraw\fabrica-agentica-visao-geral-v2.excalidraw` | `F79659EB` | `15B459E9` |
| `excalidraw\gerenciamento-secoes-por-feature.excalidraw` | `AF13EE65` | `B0DB04F4` |
| `excalidraw\review\fase-review.excalidraw` | `1AA15877` | `A9B4C5B2` |
| `markdown\comunicacao.md` | `73E19F78` | `07753A33` |
| `markdown\decisoes\2026-11-17-encerramento-feature-bootstrapper.md` | `3E21514B` | `B16F30AE` |
| `markdown\modelos\arquiteto.md` | `71B5674D` | `D526B81A` |
| `markdown\modelos\bootstrapper.md` | `A61F7821` | `6528FC11` |
| `markdown\modelos\fábrica-agêntica-v2.md` | `61A00E04` | `136DC086` |
| `README.md` | `03BAEF7E` | `21BAB72C` |
| `scripts\destruir-secao-api.py` | `4761F13E` | `C2B66236` |
| `skills\arquiteto-destruicao.md` | `6739F099` | `6E7230FD` |
| `skills\arquiteto-regras.md` | `BB3854EB` | `5DEC52FF` |
| `skills\bootstrapper-criacao-arquiteto.md` | `9DAD9A2A` | `F6ED763F` |
| `skills\bootstrapper-encerramento.md` | `E0E9715B` | `661A33B3` |
| `skills\bootstrapper-start.md` | `3FCCB07E` | `79CE5519` |
| `markdown\decisoes\2026-11-17-encerramento-sem-reconfirmacao.md` (este) | novo | n/a (este arquivo) |

Biblioteca do box (`/home/box/agent-data/workflows/<skill>/SKILL.md`), hash antes e o que deve ficar depois do `cp` do staging (`/workspace/staging-encerramento-sem-reconfirmacao/<skill>/SKILL.md`, idêntico ao espelho do PC):
- `arquiteto-destruicao`: antes `6739F099`, depois `6E7230FD`
- `arquiteto-regras`: antes `BB3854EB`, depois `5DEC52FF`
- `bootstrapper-criacao-arquiteto`: antes `9DAD9A2A`, depois `F6ED763F`
- `bootstrapper-encerramento`: antes `E0E9715B`, depois `661A33B3`
- `bootstrapper-start`: antes `3FCCB07E`, depois `79CE5519`

Descrição do app do Bootstrapper: antes `A61F7821` (`/workspace/staging-bootstrapper-secao/bootstrapper-descricao-app.md`), depois `6528FC11` (`/workspace/staging-encerramento-sem-reconfirmacao/bootstrapper-descricao-app.md`, igual a `markdown\modelos\bootstrapper.md`).

## Backup
- PC: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\encerramento-sem-reconfirmacao-20261117-1802` (arquivos em `pc\`, hashes em `hashes-antes.txt` e `hashes-antes-depois.txt`, script de edição `edit_pc_semreconf.py`).
- Box: `/workspace/backups/box-encerramento-sem-reconfirmacao-20261117-1803` (cinco skills, descrição do app e hashes antes).

## Verificação
- `py -3 -m unittest discover` em `scripts`: 69 testes, OK. `py_compile` do script: OK.
- Diagramas relidos como JSON; nenhuma fonte da V2 diz mais que o Bootstrapper reconfirma com o humano no caso do handoff do Arquiteto.
- V1 e `GrokBot-Scripts` não tocados. Sem commit.

## Pendências
- Copiar as cinco skills do staging para a biblioteca do box (`cp` e conferir o sha256) e trocar a descrição do Bootstrapper no app.
- Os diagramas só foram validados como JSON, sem renderização visual.
