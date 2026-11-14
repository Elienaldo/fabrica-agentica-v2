# Seção por fase no Supervisor e ajustes de 12–13/11/2026

**Data:** 2026-11-13 (America/Bahia, UTC-3).
**Estado:** as três decisões estão aplicadas. A decisão 1 foi esclarecida e aplicada em 13/11/2026 às 12:35 Bahia (ver Atualizações).
**Escopo desta entrega:** só este registro de decisão. Nenhuma regra, skill, descrição de bot ou ficha foi alterada por esta entrega.

## Decisão 1 — Conversa nova por fase no Supervisor

O Supervisor fecha a conversa (ou grupo) de cada fase e abre uma nova para a próxima: research, plan, implement, review, PR, dev/prod e demais. A seção da sidebar continua uma por feature (seções 18 e 23 de `supervisor-criacao-secao`); o que é por fase é a conversa, grupo ou sessão, nunca a seção da sidebar.

**Justificativa:** quem lê uma fase nova não precisa reler o conteúdo inteiro da seção anterior. Isso reduz o contexto relido e os tokens de cache, alinhado à regra 28 (conversa nova por fase e handoff enxuto).

### Regras
- Cada fase tem a sua conversa ou grupo. A conversa da fase anterior é fechada antes de abrir a próxima.
- A seção da sidebar não muda: uma por feature, criada pelo `criar-secao-feature.py`. Script de criação, pedido de bots ao Dr. Eggbot e destruição seguem como estão.
- O handoff entre seções leva só a decisão tomada e o link (ou caminho) do artefato, como manda a regra 28.
- Esta decisão não remove gates, autorizações nem validações humanas existentes.
- Pela regra de ouro, aplicar esta decisão exige atualizar no mesmo trabalho a biblioteca carregável do Supervisor (box e espelho em `skills\`), a ficha `markdown\modelos\supervisor.md` e este registro, com backup, hashes antes e depois e releitura.

## Decisão 2 — Três correções de documentação (13/11/2026)

1. **Skill e descrição:** a documentação falava em skill como se todo bot tivesse uma. Corrigido: só o Supervisor tem skills; os demais bots usam a descrição (e a ficha em `markdown\modelos\`) como biblioteca.
2. **Modelo do Cursor:** o README tratava o modelo do Cursor como genérico. Corrigido para grok-4.7 (reasoning_effort high, fast false, context 500k).
3. **Arquivo antigo de regras do Supervisor:** referências do tipo "seção N de supervisor-regras" apontavam para o arquivo único antigo. Corrigido para a skill de camada 2 certa, em 14 documentos e fichas e nas fontes reais (descrições do Supervisor, Dr. Eggbot e Dev Expresso; skill `supervisor-destruicao` no box e no PC). Registros antigos de auditoria ficaram como histórico.

Backups: `backups\readme-novidades-20261113-002701`, `backups\conflitos-doc-20261113-002759` e `backups\conflitos-lib-20261113-003015`.

## Decisão 3 — Divisão em etapas da biblioteca do Supervisor (12/11/2026)

As regras do Supervisor, que estavam num arquivo único de cerca de 36 KB, foram divididas em 3 camadas:
- **Camada 1:** `supervisor-regras`, enxuta (cerca de 3 KB), com o núcleo sempre válido, o gatilho de carregamento por fase e o índice.
- **Camada 2:** 8 skills por função: `supervisor-fases`, `supervisor-research`, `supervisor-review-merge`, `supervisor-criacao-secao`, `supervisor-destruicao`, `supervisor-operacao-cursor`, `supervisor-comunicacao-humana` e `supervisor-logs`.
- **Camada 3:** os documentos de fase em `markdown\fases\`.

**Justificativa:** minimizar os trade-offs entre as fases. Cada fase carrega só as regras de que precisa, em vez de carregar o arquivo inteiro.

O arquivo antigo foi preservado como `skills\supervisor-regras.md.pre-stageD`.

**Nota — onde vive a amarração entre as camadas:** a amarração das três camadas não está solta: ela vive na camada 1. A skill `supervisor-regras` (enxuta e sempre carregada) contém o gatilho de carregamento por fase. A mensagem de handoff traz o nome da fase, e a camada 1 indica qual skill da camada 2 e qual `fase-*.md` da camada 3 carregar antes de agir (por exemplo, research carrega `supervisor-research`, `supervisor-fases` e `markdown\fases\fase-research.md`). Funções sem fase (criar seção, destruir, operar o Cursor, contatar o humano, registrar tokens) carregam o bloco pela ação. A camada 1 também traz o índice que resolve cada seção para a sua skill da camada 2.

## Atualizações

- 2026-11-13 00:38 Bahia: registro criado.
- 2026-11-13 12:35 Bahia: o Elienaldo esclareceu que "seção por fase" é a conversa ou grupo por fase, não a seção da sidebar, que continua uma por feature. Esclarecimento aplicado no item 1 da regra 28 em `supervisor-fases` (box e `skills\supervisor-fases.md`) e na ficha `markdown\modelos\supervisor.md`.
- 2026-11-13 12:38 Bahia: corrigida a contradição da seção 21 de `supervisor-fases`, que dizia "uma única sessão do Cursor por feature". Agora diz uma sessão por fase, sem sessões extras para os passos preparatórios, alinhada às seções 15 e 28. A ficha `supervisor.md` já estava coerente e não mudou.
- 2026-11-13 13:28 Bahia: adicionada na decisão 3 a nota de que a amarração entre as três camadas vive na camada 1 (gatilho de carregamento por fase em `supervisor-regras`). A biblioteca já trazia esse gatilho e não precisou mudar.
- 2026-11-13 14:16 Bahia: diagramas Excalidraw atualizados com o grupo novo por feature, o research sem handoff de entrada e o handoff enxuto nas demais fases (ver "Atualização 13/11 — diagramas").
- 2026-11-13 14:23 Bahia: nomes dos grupos definidos: grupo inicial com o prefixo do caminho e `<fase>-<nome-da-feature>` para os de fase (ver "Atualização 13/11 — nome dos grupos").
- 2026-11-13 14:26 Bahia: decisão provisória de nomear o grupo inicial pelo prefixo do caminho (padrão ou expresso); substituída às 14:28.
- 2026-11-13 14:28 Bahia: grupo inicial único por feature, em qualquer caminho, inclusive no expresso: membros são o Supervisor e o humano que pediu a feature, e o nome é `canal-<nome-da-feature>`. O Dev Expresso não abre grupo inicial próprio. Diagrama principal ajustado: "SUPERVISOR (também no caminho expresso)" e "GRUPO INICIAL DA FEATURE (Supervisor + humano solicitante)". Os grupos de fase continuam `<fase>-<nome-da-feature>`. Skill `supervisor-fases`, descrições do Dr. Eggbot e do Dev Expresso, espelho `skills\supervisor-fases.md` e fichas `supervisor.md`, `dr-eggbot.md` e `dev-expresso.md` receberam o nome dos grupos de fase (backup `backups\lib-nomes-grupo-20261113-142836`).

## Atualização 13/11 — diagramas

Decisão do Elienaldo (13/11/2026), aplicada só nos diagramas Excalidraw. Base: regra 28 (conversa nova por fase e handoff enxuto). O restante de cada diagrama ficou como estava; só foram acrescentados elementos novos, sem sobrepor os existentes.

- **`excalidraw\fábrica-agentica.excalidraw` (fluxo completo):** novo bloco "INÍCIO DE CADA FEATURE" à esquerda do painel do research. Ao receber uma feature, o Supervisor (também no caminho expresso, conforme a decisão das 14:28) cria antes de tudo um grupo novo só com ele e o humano que solicitou a feature, e toda a comunicação daquela feature segue por esse grupo. Motivo anotado: zera o contexto e o histórico do chat sem apagar o bot (não existe reset de chat no app; um grupo novo com um só bot começa vazio). Uma seta leva o pedido do humano (a semente) ao research. Os três handoffs entre painéis ganharam a nota "decisão + link/caminho do artefato; nada colado". Os quatro painéis de fase receberam as mesmas mudanças dos diagramas de fase abaixo.
- **`excalidraw\research\fase-research.excalidraw`:** nova entrada "PEDIDO DO HUMANO (a semente)", ligada ao Principal. A primeira fase não tem handoff de entrada e recebe somente o que o humano passou. Uma nota da regra 28 diz que, na saída, o handoff ao PLAN leva só a decisão e o link ou caminho do design doc ou do PRD.
- **`excalidraw\plan\fase-plan.excalidraw`, `excalidraw\implement\fase-implement.excalidraw` e `excalidraw\review\fase-review.excalidraw` (este cobre PR, dev e prod):** nota "HANDOFF ENXUTO". Cada fase abre grupo ou sessão nova, e o handoff leva só a decisão tomada e o link ou caminho do artefato, nunca transcrições nem textos colados. A nota indica a entrada e a saída de cada fase. Na review, a nota lembra que o dev segue na mesma sessão da review, como já estava desenhado.

Backup: `backups\diagramas-grupo-por-feature-20261113-141326` (com `SHA256-antes.txt`). SHA256 antes → depois:
- fábrica-agentica: 021E923A → 375EEC5E
- fase-research: 3F2D3544 → 9D1143B4
- fase-plan: 05933CDE → 8465368A
- fase-implement: A2ED517E → 35F8DEE0
- fase-review: 7490EEFD → A79F4725

Não havia exports PNG ou SVG dos diagramas, e os links de `excalidraw\LINKS.md` continuam apontando para as versões anteriores. Nenhuma regra, skill, descrição de bot ou ficha foi alterada. A documentação textual (skills do Supervisor, fichas e docs de fase) ainda não fala do grupo novo por feature: isso fica pendente e exige decisão separada (regra de ouro).

## Atualização 13/11 — nome dos grupos

Decisão do Elienaldo (13/11/2026, 14:21 Bahia, corrigindo a das 14:19, que previa o prefixo `grupo-`; o prefixo foi descartado e nada chegou a ser gravado com ele):
- **Grupo de fase:** `<fase>-<nome-da-feature>`, por exemplo `research-feat-nome-da-feature`. O nome da feature é o mesmo que ela recebe ao ser criada, isto é, o nome da seção (seção 18 de `supervisor-criacao-secao`: `feat` ou `fix`, hífen e o nome em minúsculas com hífens). O formato anterior era `feat-<slug>-AAAAMMDD.<tipo>` (seção 5 de `markdown\comunicacao.md`; exemplo real: `feat-ambiente-dev-testes-locais-20261113.research`).
- **Grupo inicial da feature** (antes de qualquer fase; decisão final do Elienaldo às 14:28 Bahia): um só por feature, em qualquer caminho, inclusive no expresso, com o Supervisor e o humano que pediu. Nome: `canal-<nome-da-feature>`, por exemplo `canal-feat-nome-da-feature`.
- **Grupo de direção:** removido por decisão do Elienaldo em 13/11/2026 às 16:55 Bahia. Não existe grupo de direção. Ver "Atualização 13/11 — remoção do grupo de direção".

Aplicado em: `markdown\comunicacao.md` (seção 5), `markdown\regras\convencoes-fabrica.md` (nova seção "Nome dos grupos"), `markdown\fases\fase-research.md`, `fase-plan.md`, `fase-implement.md` e `fase-review.md` (nota no fim), e nos 5 diagramas (`fábrica-agentica`, `fase-research`, `fase-plan`, `fase-implement` e `fase-review`). Backup: `backups\nomenclatura-grupo-20261113-142105`.

Regra de ouro: o nome dos grupos de fase foi aplicado às 14:27–14:29 Bahia na skill `supervisor-fases` (seção 28, item 1), nas descrições do Dr. Eggbot e do Dev Expresso, no espelho `skills\supervisor-fases.md` e nas fichas `supervisor.md`, `dr-eggbot.md` e `dev-expresso.md`. Pendente: o grupo inicial (`canal-<nome-da-feature>`) ainda não existe como regra em nenhuma fonte carregável e entra quando a regra do grupo inicial por feature for levada à biblioteca.

## Atualização 13/11 — grupo inicial nas bibliotecas carregáveis (16:28 Bahia)

A regra do grupo inicial `canal-<nome-da-feature>` (decisão das 14:28 Bahia) entrou nas fontes carregáveis. Os docs-fonte (`markdown\comunicacao.md` §5, `markdown\regras\convencoes-fabrica.md` e as notas de grupo de fase em `markdown\fases\fase-*.md`) não foram alterados.

Já estava: o nome dos grupos de fase `<fase>-<nome-da-feature>` na skill `supervisor-fases` §28 item 1 (box e espelho do PC), nas descrições do Dr. Eggbot e do Dev Expresso e nas fichas `supervisor.md`, `dr-eggbot.md` e `dev-expresso.md`.

Alterado neste turno (regra de ouro; backup no PC `backups\comunicacao-grupos-20261113-162714` e no box `/workspace/backups/comunicacao-grupos-20261113-162714`):

- skill `supervisor-regras` (camada 1, box LF / espelho PC CRLF): o essencial cita o grupo inicial e o de fase.
  - antes `E0570B4DB34F75E4E9B5AD3D7558147933D0CC35C68713F1E2AE11F228834017` → depois `727D7D020B9AE18ED2BA3258DE9D0C29D7B4E41DB29B5501B832A5C9B14865DE` (box)
  - antes `EEE6C49F6F109E5170BBD64C8FC4F81D34BDA86EB17494C57D38989BC5C3792F` → depois `DDCED7BA1AB2474A1F6ADB3F785CD285CD751B13D9ED937D222E3EC0EE29930A` (PC)
- skill `supervisor-criacao-secao` §18: criação do grupo `canal-<nome-da-feature>` antes da branch, dos bots e de qualquer fase, inclusive no expresso.
  - antes `D859C114D6E65D76A5458AD46B1D34B1298FB16E656FEBCCCE77CABCC3FDE56D` → depois `99451F7A73C540EFF385AD55EBEAA5BF87DD49EEA24B01BC287F9930E0379B6A` (box)
  - antes `0DE696106C01B904AA9BA55703054A23EC0131E041709BB6F0B8B5A3C7DFCAD3` → depois `CF2DD9CD9F4836CF88AC69588A54B82E787BA5118F0E5B58F2D3BA44BA184A06` (PC)
- skill `supervisor-comunicacao-humana` §4: a conversa da feature com o humano ocorre nesse grupo.
  - antes `34B5B367B32A0CD6D17972996489F1A0FBFF98A4DFC24525A833457ABF12A4C6` → depois `5EE1E8DE03B870397FD824A819F90690266F1E810835A95774FDD4795C40D3E8` (box)
  - antes `029A7C8479BB0BD86CD88CDD7BFF1AAD2E924DE8CD3FAA2CB9FF54A50A74053D` → depois `00F4367B53A6B03632A1B90646B1CBEDBE678AB346F151992C2FFCC2B08E97B8` (PC)
- skill `supervisor-fases` §28 item 1: o grupo inicial não se confunde com o grupo de fase.
  - antes `E5B95F0919E5B28F7A166B168E0155A5F60FBF9693DC13339A18BD022C400B2E` → depois `FAE9D4FF3BA793DCEB9B968FC570BD6E045C232A925362B95EDC7E3D425E69A4` (box)
  - antes `918061557CC53F5A2720AB57801BB352A99D68B51218B5BBD7F2434F09191BFA` → depois `D1C24F742C7A77D6156FB837C90A677A35FA6A5111D59D319A18F6C49B88A31B` (PC)
- fichas `supervisor.md`, `dr-eggbot.md` e `dev-expresso.md`: o mesmo acréscimo do grupo inicial no item 1 da seção 28.
  - `markdown\modelos\supervisor.md` antes `ACCE2E4074F028882361B270BD440367FB081FE0F964FB22FF1742F003227264` → depois `929FBEB9D02BC168E540FC568158BC3007C3BE1753C27CB210304B15BAA3E109`
  - `markdown\modelos\dr-eggbot.md` antes `52FA45CC8C283E26D973C3E437AC5CDB6CFE2D5DCB07A2C8697C8AEAE5FB0A7C` → depois `D24326B46426889418C415333536412AA886F8D06E8A2145570FEC6C10B45DB0`
  - `markdown\modelos\dev-expresso.md` antes `E00CBDC326F42D6715B6C6B1C2DBC5931AFC14B42DFAE82947F0923E2BB70856` → depois `57D54FAE4026C700A1CCD1986E61565137B4E7DD436FAA1697A6C6E67052E315`

Verificação: as quatro skills box×PC ficaram iguais após normalizar o fim de linha (box LF, PC CRLF). O item 1 da seção 28 nas fichas do Dr. Eggbot e do Dev Expresso coincide com o texto preparado das descrições.

Pendências:
- As descrições vivas do Dr. Eggbot e do Dev Expresso ainda não foram gravadas neste turno (este executor não tem a ferramenta UpdateAgent). Textos completos preparados em `/workspace/comunicacao-grupos-descricoes-preparadas/descricao-dr-eggbot.nova.txt` (SHA256 `7E50DEE7777F0F6EB67726CFD993C7528DE9946AA1DDA89A4318E130C1E26239`; antes `E1871A3BD32C5D2869EED7BA064DF6EF2B3ADD1C409C2A9AD4F2FEF705E5CB8A`) e `descricao-dev-expresso.nova.txt` (SHA256 `6BF3A4DBEC725404947BBB7888D9093C3D68451EBE48471CDAD2A5EB7269AC1B`; antes `B49F52DD3B864AE03F4BBCEFAC7522871528BACA4882CC7E6192E384686A6063`). Até o UpdateAgent, descrição viva e ficha ficam em versões diferentes.
- O grupo de direção foi removido por decisão do Elienaldo em 13/11/2026 às 16:55 Bahia (ver atualização abaixo). Não permanece pendente.
- Demais bots (Principal Product Engineer, Product Engineer, Design de front-end, Advogado do diabo, Orquestrador etc.) citam o grupo de research ou o roteamento pelo Supervisor, mas não a nomenclatura; não foram editados, porque não criam o grupo inicial nem definem o nome dos grupos.

## Atualização 13/11 — Principal acorda votantes no brainstorm (16:52 Bahia)

Pedido do Elienaldo (13/11/2026, 16:49 Bahia): no brainstorm, sempre que o Principal Product Engineer estiver aguardando o voto de qualquer membro da equipe, ele avisa e acorda esse membro no mesmo turno, com mensagem direta (SendToAgent com prioridade), para o debate não ficar parado com gente dormindo. Não cria rotina nem listener.

Fonte real: descrição do bot permanente Principal Product Engineer (`cbe572c8-e333-4b13-bfc4-455da5928641`). Não há skill do Principal em `/home/box/agent-data/workflows/`. Não há outro agente Principal na feature em curso (`feat-ambiente-dev-testes-locais`; grupo de research `7b33ce62-1df7-42c5-a008-57ac1880f8d5`): os membros são os bots permanentes (Principal, Product Engineer, Design de front-end e Advogado do diabo). A descrição viva já traz o escopo desta sessão; a ficha permanece o modelo, sem esse escopo e sem o cabeçalho de IA externa.

O trecho novo entrou na Regência da ficha e da descrição preparada (texto idêntico nos dois), e o item 2 da Regência foi ajustado para somar o aviso direto à cobrança no grupo, sem duplicar a regra.

Aplicado (regra de ouro; backup no PC `backups\principal-acordar-votantes-20261113-165135` e no box `/workspace/backups/principal-acordar-votantes-20261113-165135`):

- ficha `markdown\modelos\principal-product-engineer.md`
  - antes `D8B1F0D6978464A464D524E2C3438D13E01C266BB4A4024635DAF1530F2349F6` → depois `FB0D9DA67FF4522476746535BC71CE2EF7F46A5FA6AA5CB37E5E693886B64E9B`
- `markdown\fases\fase-research.md`: o fluxo de votação passa a exigir o aviso direto do Principal, sem substituir o debate no grupo.
  - antes `DF5EDDE14D611E5ECEAB30E9B0D99ACD85912EAF6D3BD009B7F245CA4D99798B` → depois `54EA49ABF153D728AED6918345109ED2E93D9C35FA4D51F88FDB514B1732056A`
- skill `supervisor-research` (box LF / espelho PC CRLF): o Principal, ao aguardar voto, faz o aviso direto; isso não transfere a cobrança ao Supervisor nem substitui o debate no grupo.
  - antes `6792BA578FA249866E6E2E9AB1067D4A3009A7D3EFC7CD22F72166226A1B4352` → depois `E5856356FBEA451A783D90B4AF477DE5D49B2233D8876810F75336F062EDDF1A` (box)
  - antes `F87C9FD0C364F8703CAD272D7F4B3DBE73467281E302AB117932B30D34DFB14C` → depois `62B8CAFC092E1066C7D24D0066B8549722CC6E0FE2D892B96775EA1A010E6E1F` (PC)

Verificação: skill box×PC iguais após normalizar o fim de linha. O parágrafo novo da Regência na ficha coincide com o da descrição preparada.

Pendência: a descrição viva do Principal ainda não foi gravada neste turno (este executor não tem a ferramenta UpdateAgent). Texto completo preparado em `/workspace/principal-acordar-votantes/descricao-cbe572c8-e333-4b13-bfc4-455da5928641.nova.txt` (SHA256 `44E4D116248CDF849416590D5EC27F0C1AF5F4E47E521D15E552D0E736B71670`; antes `B57F0BEC273CBB07E8C6F659B61EE9CDB1D2EBF69BA74B51F244C83EE19FB7F2`). Até o UpdateAgent, descrição viva e ficha ficam em versões diferentes.

## Atualização 13/11 — remoção do grupo de direção (16:55 Bahia)

Decisão do Elienaldo (13/11/2026, 16:55 Bahia): não existe grupo de direção na Fábrica Agêntica. A comunicação é: (1) o canal `canal-<nome-da-feature>` entre o Supervisor e o humano (Elienaldo); (2) um grupo por fase de cada feature, `<fase>-<nome-da-feature>`, onde ficam o Supervisor, o Orquestrador e os bots da fase. Tudo o que passava pelo grupo de direção (Supervisor↔Principal, Supervisor↔Orquestrador, entrega de insumos, pedidos ao Cursor, falhas e escaladas) passa a acontecer no grupo da fase em curso. O conceito foi removido por completo, não apenas o formato do nome.

Consequência alinhada, sem regra nova além disso: o grupo de review deixou de ser criado com a sessão. Como os demais grupos de fase, ele abre quando a fase review começa. O grupo de research continua nascendo junto com os agentes de research, quando o Principal classifica a feature como SIM. O Supervisor continua fora do debate dos quatro no grupo de research; a entrega de insumos e o resultado do research passam pelo Principal.

O grupo já existente `feat-ambiente-dev-testes-locais-20261113.direção` (id `8c993137-0392-4c0e-a418-e7032a645c89`) não foi apagado: a exclusão depende de autorização humana explícita. O casamento legado `<feature>-AAAAMMDD.direção` no script `destruir-secao-api.py`, na skill `supervisor-destruicao` e no `contratos/contrato-destruicao-api-interna.md` permanece, só para limpar grupos antigos.

Aplicado (regra de ouro; backup no PC `backups\remove-direcao-20261113-165953` e no box `/workspace/backups/remove-direcao-20261113-165953`):

- `markdown\comunicacao.md`: removeu o grupo de direção da criação, da tabela, dos pares e do roteamento; o review abre com a fase, não com a sessão; o canal da feature entrou na tabela.
  - antes `4F99293CCAD9C93E5075C39FD584963560D0F97DD823299A984D87E51B813993` → depois `6606F630F8980CC07EE3DC08F32F0247E2482A5BA881917F73FF346FFB1A269A`
- `markdown\regras\convencoes-fabrica.md`: a seção "Nome dos grupos" registra que não existe grupo de direção.
  - antes `1609E7B41982937EEAFDF7CD8844F6FCB6F052742B1698CC59CE55EC33BBC6CC` → depois `AFED1A883E886F0ECAD7376F5AD17CE7447184A2B284CF4FF33D2D4358160B62`
- skill `supervisor-research` (box LF / espelho PC CRLF): a entrega de insumos ao Principal deixou de citar o canal de direção.
  - antes `E5856356FBEA451A783D90B4AF477DE5D49B2233D8876810F75336F062EDDF1A` → depois `47EDFD48AD4BA31CFF7C2C0F7F3CD1FEADA9F254C51A14B34E1588D777E44A69` (box)
  - antes `62B8CAFC092E1066C7D24D0066B8549722CC6E0FE2D892B96775EA1A010E6E1F` → depois `70B676DD64C73A168EBA8750FA31E713B64DFC4085A3A773E3A5047BC8EEA461` (PC)
- `README.md`: o resumo de `comunicacao.md` passou a falar em canal da feature e grupos por fase.
  - antes `D680D35C4F17A85DD592B25D7BFBDF9FC0BF776BDB8E11704A1DD3276E23DD65` → depois `A463EC9FA8838815415AC830DD3E595B2EC57BE22FBF27B779E28889EEE8FA33`

A descrição viva do Orquestrador de pipeline (`9fcc9a24-bca6-424a-998d-cd90936b283d`) ainda cita o grupo de direção no escopo desta sessão; este executor não tem UpdateAgent. Texto completo preparado em `/workspace/remove-direcao/descricao-9fcc9a24-bca6-424a-998d-cd90936b283d.nova.txt` (SHA256 `7B1F34F1591CE2A8B6230086C6A194EA2F19C8EE8D72C96255A3BEA72F6B1313`; antes `E0744B826A281BD4A2827DE81FF07820259BB26ADF8B06945524523F21B5835D`). A ficha `orquestrador-de-pipeline.md` é o modelo, sem o escopo da sessão e já sem o conceito de direção; não foi alterada.

Verificação: skill box×PC iguais após normalizar o fim de linha. Excalidraw, fichas e `markdown\fases\*.md` já estavam limpos (sem o conceito de grupo de direção).
