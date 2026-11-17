# Decisão: o Bootstrapper passa a encerrar a feature (desenho A)

**Data:** 17/11/2026, à tarde (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras
**Atualização (17/11/2026, ~17:59, Bahia):** o passo 4 do desenho (confirmação direta do humano) deixou de valer para o handoff do próprio Arquiteto da seção; ver `2026-11-17-encerramento-sem-reconfirmacao.md`. O restante da decisão segue.

## O que foi decidido
O encerramento da feature (excluir o Arquiteto, depois a seção, depois os grupos de fase) passa a ser responsabilidade do Bootstrapper, só na Fábrica Agêntica V2. O Arquiteto só avisa o Bootstrapper, depois da autorização humana explícita. A V1 e o `GrokBot-Scripts` não foram tocados.

## Motivo
O Arquiteto rodava `destruir-secao-api.py` no próprio Shell. Na etapa 4 o script exclui o Arquiteto, o processo morria junto e as etapas 5 (seção) e 6 (grupos) nunca rodavam; a seção `section-mwktbk4s-1` ficou viva. A ordem do script não muda. Quem pode rodar o script inteiro é um bot que não seja excluído por ele: o Bootstrapper, que é fixo e permanente.

## Desenho
1. O humano autoriza o encerramento ao Arquiteto.
2. O Arquiteto envia ao Bootstrapper o handoff: `feature`, `secao_id`, `arquiteto_id`, `grupos` (`id=nome` dos grupos `<fase>-<feature>`), `autorizacao_texto`, `autorizacao_hora` (Bahia) e `escopo`. O Arquiteto não exclui nada, nem a si mesmo, e não roda o script.
3. O Bootstrapper valida: `ListSections` (nome exato e id da seção) e dry-run do script (só aquele Arquiteto como alvo, nenhum protegido, plano de grupos igual ao do handoff).
4. O Bootstrapper confirma direto com o humano, com o alvo e o alcance. A autorização repassada por um bot não vale como aprovação. (Substituído em 17/11/2026, ~17:59: para o handoff do próprio Arquiteto da seção não há nova confirmação; ver a atualização no topo.)
5. O Bootstrapper roda o script com `--api-real --executar` e as confirmações exatas (`--confirmar-exclusao`, `--confirmar-bots`, `--confirmar-grupos`), uma vez.
6. O Bootstrapper lê o resultado e avisa o humano.

## O que mudou
- `scripts\destruir-secao-api.py`: fluxo, etapas e flags iguais. Docstrings agora dizem que o Bootstrapper dispara e controla o script. Removido o aviso automático por webhook ao Bootstrapper (ele avisaria a si mesmo); o resultado (`needs_human_notification`, `erro`, `motivos_aviso_humano`) continua no JSON e no log.
- Testes: `IntegracaoDestruicaoTest` reescrito para provar que nenhuma notificação é enviada (69 testes, todos OK). `notificacao_bootstrapper.py` ficou sem chamador (módulo e testes mantidos).
- `skills\arquiteto-destruicao.md`: virou o aviso de encerramento ao Bootstrapper (mesmo arquivo e mesma seção 24; mudaram o `name`, a descrição e o título).
- `skills\bootstrapper-encerramento.md`: skill nova com o recebimento do handoff, a validação, a confirmação, a execução e o relatório.
- `skills\arquiteto-regras.md`, `skills\bootstrapper-start.md`, `skills\bootstrapper-criacao-arquiteto.md`: regras, gatilhos e limites ajustados.
- Fichas: `markdown\modelos\bootstrapper.md` (papel 2 novo, no lugar de "Não aceita nem executa destruição..."), `markdown\modelos\arquiteto.md` e `markdown\modelos\fábrica-agêntica-v2.md`.
- Documentos: `contratos\contrato-destruicao-api-interna.md`, `contratos\contrato-webhook-destruicao.md` (reescrito, sem webhook), `contratos\execucao-verificacao\fluxo-contrato-verificacao.md`, `markdown\comunicacao.md`, `markdown\regras\convencoes-fabrica.md` e `README.md`.
- Diagramas `.excalidraw` (só texto e setas necessárias, JSON válido e vínculos conferidos): `destruicao-api-interna`, `gerenciamento-secoes-por-feature`, `fábrica-agentica`, `acompanhamento\acompanhamento-comunicacao`, `contrato\fluxo-contrato-verificacao`, `review\fase-review`, `fabrica-agentica-visao-geral` e `fabrica-agentica-visao-geral-v2`.

## Arquivos e hashes (SHA-256, 8 primeiros caracteres)
- `README.md`: `10FF6F39` antes, `03BAEF7E` depois.
- `contratos\contrato-destruicao-api-interna.md`: `A2EEDEAA` antes, `3E754B87` depois.
- `contratos\contrato-webhook-destruicao.md`: `3F8C79D9` antes, `D1AE66E3` depois.
- `contratos\execucao-verificacao\fluxo-contrato-verificacao.md`: `1E4C3BDD` antes, `2B0EDEED` depois.
- `excalidraw\acompanhamento\acompanhamento-comunicacao.excalidraw`: `C8D146DC` antes, `7054798E` depois.
- `excalidraw\contrato\fluxo-contrato-verificacao.excalidraw`: `F4F1070F` antes, `28BC71CC` depois.
- `excalidraw\destruicao-api-interna.excalidraw`: `055F509E` antes, `188660FC` depois.
- `excalidraw\fabrica-agentica-visao-geral-v2.excalidraw`: `A15F8E18` antes, `F79659EB` depois.
- `excalidraw\fabrica-agentica-visao-geral.excalidraw`: `DF509AB6` antes, `5BA48254` depois.
- `excalidraw\fábrica-agentica.excalidraw`: `ED5E98B6` antes, `4E9AAE3D` depois.
- `excalidraw\gerenciamento-secoes-por-feature.excalidraw`: `9BAF59C3` antes, `AF13EE65` depois.
- `excalidraw\review\fase-review.excalidraw`: `91775A22` antes, `1AA15877` depois.
- `markdown\comunicacao.md`: `BC86CAB1` antes, `73E19F78` depois.
- `markdown\modelos\arquiteto.md`: `89024DEB` antes, `71B5674D` depois.
- `markdown\modelos\bootstrapper.md`: `7CCF38A6` antes, `A61F7821` depois.
- `markdown\modelos\fábrica-agêntica-v2.md`: `0547C109` antes, `61A00E04` depois.
- `markdown\regras\convencoes-fabrica.md`: `423EFCE0` antes, `A25BC843` depois.
- `scripts\destruir-secao-api.py`: `C9F47F38` antes, `4761F13E` depois.
- `scripts\notificacao_bootstrapper.py`: `2186A040` antes, `372F397A` depois.
- `scripts\test_destruir_secao_api.py`: `72916D93` antes, `CC3FA4DF` depois.
- `scripts\test_notificacao_bootstrapper.py`: `1AA8C45A` antes, `47950DF3` depois.
- `skills\arquiteto-destruicao.md`: `F568146D` antes, `6739F099` depois.
- `skills\arquiteto-regras.md`: `A4FEA7A8` antes, `BB3854EB` depois.
- `skills\bootstrapper-criacao-arquiteto.md`: `82EC480C` antes, `9DAD9A2A` depois.
- `skills\bootstrapper-start.md`: `C60C0B7A` antes, `3FCCB07E` depois.
- `skills\bootstrapper-encerramento.md` (novo): `E0E9715B` depois.
- Backup no PC: `Fabrica-Agentica-backups\encerramento-feature-bootstrapper-20261117-1703` (arquivos do PC em `pc`, cópias da biblioteca do box em `box`). Os dois `visao-geral` foram salvos depois, a partir do `HEAD` do git (o conteúdo era idêntico, só havia diferença de arredondamento numérico).

## Pendências
- A biblioteca do box precisa receber o conteúdo preparado em `/workspace/staging-bootstrapper-secao` (`arquiteto-destruicao`, `arquiteto-regras`, `bootstrapper-start`, `bootstrapper-criacao-arquiteto` e a skill nova `bootstrapper-encerramento`, que exige um diretório novo).
- A descrição do bot Bootstrapper no app deve ser trocada pelo texto de `/workspace/staging-bootstrapper-secao/bootstrapper-descricao-app.md`.
- A rotina "Fábrica V2 — bloqueio destruição" não tem mais chamador; o humano pode desativá-la. A rotina "Fábrica V2 — bloqueio criação" continua em uso.
- Os diagramas só foram validados como JSON e por vínculos, sem renderização visual: vale abrir e conferir o layout. Não há PNG nem SVG exportados na V2.
- `checklist-v2.html` guarda o histórico antigo (cita a destruição como era); não foi alterado.
- Sem commit.
