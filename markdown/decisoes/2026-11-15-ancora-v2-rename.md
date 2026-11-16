# Decisão: renomear as referências ao bot Âncora da V2 para "Âncora V2"

**Data:** 15/11/2026, por volta das 22h13 (horário da Bahia)
**Decisão de:** Elienaldo, por voz
**Executado por:** Mestre de obras

## O que foi decidido
O bot Âncora da seção Fábrica Agêntica V2 (`3aa31f55…`) foi renomeado no app para "Âncora V2". As referências da V2 a esse bot passam a dizer "Âncora V2". O que fala do Âncora da V1, e o que for ambíguo, ficou como estava.

## Arquivos alterados
| Arquivo | Trocas | SHA-256 antes | SHA-256 depois |
|---|---|---|---|
| `README.md` | 5 | `C56FE3C5…` | `4020F84C…` |
| `contratos/contrato-webhook-criacao.md` | 3 | `C5DB6E4B…` | `B9A4BC0B…` |
| `scripts/criar-secao-feature.ps1` | 12 | `08FDCEB8…` | `04662B12…` |
| `scripts/criar-secao-feature.py` | 4 | `B3CEA119…` | `99BA5D44…` |

- A codificação foi mantida: o `.ps1` continua UTF-8 com BOM, os outros continuam sem BOM, e todos seguem com quebra de linha LF.
- `criar-secao-feature.ps1`: o script procura o bot pelo nome exato (`-ceq $AnchorName`). Por isso `$AnchorName` passou de `'Âncora'` para `'Âncora V2'`. Sem essa troca, o script não acharia o bot renomeado. As mensagens e o comentário que citam o bot também passaram a dizer "Âncora V2".
- `criar-secao-feature.py`: o nome reservado passou de `"âncora"` para `"âncora v2"`, igual ao `.ps1`, que reserva `$AnchorName`. A descrição e a mensagem de erro também foram atualizadas.

## Conferência
- Releitura de cada arquivo comparada com o backup: só mudaram as linhas que citam o bot.
- O `.ps1` foi analisado pelo parser do PowerShell sem executar, com 0 erros.
- `feature_name` reserva "Âncora V2" em qualquer caixa e aceita "Âncora".
- Os testes puros da pasta `scripts` (`unittest`) rodaram 69 testes, todos OK. Nenhum bot nem seção foi criado, movido ou apagado.
- Não ficou `__pycache__`.

## Backup
`Fabrica-Agentica-backups\ancora-v2-rename-20261115-2213`, com os 4 arquivos originais. Os hashes do backup conferem com os de antes.

## Não alterado
- `checklist-v2.html:128` e `:131`: citam o Âncora explicitamente entre os bots da V1.
- `markdown/regras/convencoes-fabrica.md:65`: diz "Descrições vivas atualizadas: Dev Expresso, Dr. Eggbot, Grok Bot, Âncora, Mestre de obras". É ambíguo, porque é registro histórico e não diz qual Âncora.
- `markdown/decisoes/2026-11-15-fixos-api-client-sem-v1.md:8`: diz "Ancora (`9b3c5289…`)". É registro histórico com o ID do outro Âncora.
- `markdown/decisoes/2026-11-15-ancora-v2-fixo-api-client.md` e a linha de `FIXOS_POR_ID` em `scripts/grokbot_api_client.py`: tratados à parte e não tocados aqui.
- Os diagramas `.excalidraw` da V2, as skills em `V2/skills` e as skills `bootstrapper-*` e `arquiteto-*` do box não citam o Âncora. Nenhuma skill mudou.

## Observação
`criar-secao-feature.ps1` usa `$Origin='Fábrica Agêntica'` e exige o nome exato do cabeçalho da seção. Se a seção no app se chama "Fábrica Agêntica V2", o script não acha a seção de origem. Isso não foi alterado e fica para decisão do humano.

## Commit
Não houve commit.