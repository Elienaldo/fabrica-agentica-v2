# Decisão: ponteiro da mensagem de autorização no handoff de encerramento

**Data:** 20/11/2026 (horário da Bahia)
**Pedido de:** Elienaldo (por voz)
**Executado por:** Mestre de obras
**Complementa:** `2026-11-17-encerramento-sem-reconfirmacao.md` (as travas a, b, c e d continuam; entra a trava e).

## Problema
O Arquiteto avisou o Bootstrapper com o handoff (feature, secao_id, arquiteto_id, grupos, autorizacao_texto, autorizacao_hora, escopo), mas o Bootstrapper não conseguiu identificar a autorização do humano e pediu de volta.

## O que foi decidido
O handoff ganha o campo `autorizacao_ref`, o ponteiro da mensagem exata em que o humano autorizou, em uma linha:
`conversa=<arquiteto_id>; posicao=<número>; hora_iso=<AAAA-MM-DDThh:mm:ss-03:00>`
- `conversa`: o id do Arquiteto (a conversa que o Bootstrapper vai ler).
- `posicao`: o número `position` que o `SearchTranscripts` devolve no histórico do próprio Arquiteto para a mensagem do humano.
- `hora_iso`: a hora dessa mensagem, em ISO 8601 com fuso; `autorizacao_hora` passa a ser escrita no mesmo formato.
O id curto de mensagem do turno (do tipo `t12u`) NÃO é lido pelas ferramentas de transcrição e não é usado como ponteiro nem como prova.

## Como a leitura foi verificada (só leitura, 20/11/2026)
- `ReadTranscript` e `SearchTranscripts` (namespace `cursor.bot`) aceitam `in=<id de outro bot do mesmo dono>`. Teste feito no histórico do Bootstrapper por um bot do mesmo dono.
- A busca devolve o `position` e a origem de cada mensagem; `ReadTranscript` com `around=<position>` devolve exatamente aquela mensagem (conferido).
- Cada mensagem de usuário traz `speaker` e `speakerId`: o humano aparece como `cu:<número>`; um bot que escreve aparece como `agent:<id>`. Isso permite separar mensagem do humano de mensagem repassada por bot.
- `after` e `before` filtram por hora: uma janela de 10 minutos em volta do evento achou a mensagem; uma janela posterior ao evento não achou nada. As ferramentas NÃO mostram a hora de cada mensagem; a hora se prova pela janela de busca.

## Regra de validação do Bootstrapper (trava e, só leitura, antes de executar)
1. `autorizacao_ref` completo; `conversa` = `arquiteto_id` = remetente; `hora_iso` = mesmo instante de `autorizacao_hora`.
2. `ReadTranscript in=<arquiteto_id> around=<posicao>`: a mensagem é `user`, `speakerId` `cu:` (o mesmo humano dono; nunca `agent:`) e contém literalmente `autorizacao_texto`.
3. `SearchTranscripts in=<arquiteto_id>` com `after`/`before` de mais ou menos 5 minutos em volta de `hora_iso`: a mesma posição aparece, com origem `cu:`.
4. Se a autorização for curta ("sim"), a mensagem do Arquiteto imediatamente anterior é a pergunta de encerramento e o alcance dela bate com `escopo` e `grupos`.
5. Nenhuma mensagem posterior do humano cancela, restringe ou contradiz.
6. Posição que não confere: uma única busca por texto literal na janela; só segue se houver exatamente uma mensagem `cu:` batendo.
7. Qualquer falha (ponteiro faltando ou malformado, leitura indisponível, mensagem inexistente, de bot, texto ou hora diferentes, alcance maior que o autorizado, revogação, mais de um candidato): PARA e pergunta ao humano. Salvaguardas anteriores mantidas: remetente = `arquiteto_id` dentro de `secao_id` (`ListSections`), dry-run obrigatório, ordem fixa Arquiteto, seção e grupos, divergência pára.
8. Lê só o histórico do `arquiteto_id`, só o necessário; registra posição, `hora_iso`, prefixo `cu:` e resultado, sem copiar trechos longos nem segredos.

## Como o Arquiteto monta o ponteiro
Busca a resposta do humano no próprio histórico (`SearchTranscripts` sem `in`), escolhe o resultado de origem `cu:`, confirma com `ReadTranscript around`, e preenche o campo. Se não localizar, não inventa e não envia o handoff: avisa o humano e pede que confirme de novo na conversa com ele.

## Pendências e riscos (não verificados nesta rodada)
- O Arquiteto fala com o humano no grupo da fase (`<fase>-<feature>`). Não foi testado se as mensagens do grupo aparecem no histórico do Arquiteto lido por `in=<arquiteto_id>`, nem se o `position` visto pelo próprio Arquiteto (sem `in`) é o mesmo visto pelo Bootstrapper (com `in`). Se não for, a trava e pára e o Bootstrapper pergunta ao humano (comportamento seguro, mas volta a pedir). Recomenda-se um teste com um Arquiteto de teste real antes de confiar no fluxo.
- O Bootstrapper ler o histórico de um Arquiteto criado dinamicamente depende de o Arquiteto ter o mesmo dono; só foi testado Mestre de obras lendo o Bootstrapper.
- Acréscimo desta rodada, de decisão do executor: a verificação de revogação por mensagem posterior do humano (item 5).

## O que mudou
- Skills (biblioteca carregável e espelho no PC): `arquiteto-destruicao` (principal), `bootstrapper-encerramento` (trava e), `arquiteto-regras`, `bootstrapper-start`.
- Fichas: `markdown\modelos\arquiteto.md`, `bootstrapper.md`, `fábrica-agêntica-v2.md`.
- Contratos: `contrato-destruicao-api-interna.md`, `contrato-webhook-destruicao.md`, `fluxo-contrato-verificacao.md`.
- `README.md`; diagramas `fase-review` e `fábrica-agentica` (só o texto do quadro FIM DA FEATURE).
- Não alterados: o script `destruir-secao-api.py` (o ponteiro é conferido pelo Bootstrapper, não pelo script) e as decisões antigas.
- Descrição do Bootstrapper no app: o modelo `bootstrapper.md` mudou; a descrição no app precisa ser atualizada para bater.

## Arquivos e hashes (SHA-256, 8 primeiros caracteres; ajustes 1 e 2 juntos)
| Arquivo (V2) | Antes | Depois |
| --- | --- | --- |
| `skills\arquiteto-destruicao.md` | 6E7230FD | 58FE2B7E |
| `skills\bootstrapper-encerramento.md` | 661A33B3 | 9FC757E4 |
| `skills\arquiteto-review-merge.md` | 036C57BC | F415A76F |
| `skills\arquiteto-comunicacao-humana.md` | 57728DE7 | B42A11AD |
| `skills\arquiteto-regras.md` | 5DEC52FF | 1155BC26 |
| `skills\bootstrapper-start.md` | 79CE5519 | 0701601E |
| `markdown\modelos\arquiteto.md` | D526B81A | 494F0316 |
| `markdown\modelos\bootstrapper.md` | 6528FC11 | 3040D55B |
| `markdown\modelos\fábrica-agêntica-v2.md` | 136DC086 | 0DF671D8 |
| `README.md` | 21BAB72C | 973641E5 |
| `markdown\fases\fase-review.md` | F9A43656 | CF700805 |
| `contratos\contrato-destruicao-api-interna.md` | 42070AD0 | 026D83C9 |
| `contratos\contrato-webhook-destruicao.md` | 122AF579 | ECFBB2C8 |
| `contratos\execucao-verificacao\fluxo-contrato-verificacao.md` | F3AE0CC0 | 0C6658F5 |
| `excalidraw\review\fase-review.excalidraw` | A9B4C5B2 | CAA2E84A |
| `excalidraw\fábrica-agentica.excalidraw` | 02ED0D4D | CE3B1076 |

Backup do PC: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\ponteiro-autorizacao-20261120-1236`. Backup do box: `/workspace/backups/box-ponteiro-autorizacao-20261120-1237`.
