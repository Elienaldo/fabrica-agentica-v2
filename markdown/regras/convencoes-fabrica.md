# Convenções da fábrica agêntica

**Data:** 2026-11-02

## Branches

Toda nova solicitação cria uma branch nova. Nunca se reutiliza branch de outra solicitação.

**Padrão de nome:** `feat/YYYYMMDD-nome-da-task`

- `feat` é a abreviação de feature.
- `YYYYMMDD` é ano, mês e dia.
- `nome-da-task` é o slug gerado automaticamente pelo supervisor a partir das palavras principais da solicitação, sem artigos e preposições, com até uns três termos e hífen entre eles. O slug é o mesmo nome da task.

**Exemplo:** `feat/20261102-botao-login`

**Por quê:** isola uma solicitação da outra e deixa o merge limpo.

## Roteamento

O grupo de chat amarra o projeto. Se o pedido for de outro projeto, o supervisor pergunta antes de rotear.

## Campos que a notificação de conclusão não traz

A notificação de conclusão do agente de nuvem não traz o campo tipo nem o slug de origem. Os dois vêm do Supervisor, que os registra no livro-razão ao lançar o agente e os recupera pelo ID do agente. Quem preenche esses campos é o Supervisor, não o agente que roda. Não há webhook no fluxo.

## Criação de bots: sempre pelo modelo

Existe um modelo para cada bot da fábrica, em `C:\Users\Elienaldo\Projetos\Fabrica-Agentica\markdown\modelos\` (por exemplo `supervisor.md`, `dr-eggbot.md`, `principal-product-engineer.md`, `orquestrador-de-pipeline.md`, `cirurgiao.md`, `curador-amigavel.md`).

**Regra (decidida pelo Elienaldo em 2026-11-03):** sempre que o Dr. Eggbot receber uma solicitação de criação de bot na fábrica, ele usa o modelo correspondente àquele bot e o aplica na criação: nome, job único, anti-jobs, voz, quando acorda e como concreto. Não cria um bot da fábrica de cabeça nem a partir de descrição solta no pedido.

- Quem pede a criação indica o modelo pelo nome do arquivo.
- Se não existir modelo para o bot pedido, o Dr. Eggbot não cria: devolve o pedido e avisa o Elienaldo.
- Se o pedido contradisser o modelo, vale o modelo; a divergência vai ao Elienaldo antes de criar.
- O Dr. Eggbot busca diretamente o arquivo do modelo do bot em `C:\Users\Elienaldo\Projetos\Fabrica-Agentica\markdown\modelos\`. Só se não conseguir acessar o arquivo, por qualquer motivo, ele pede o texto do modelo a quem fez o pedido (Supervisor ou Mestre de obras). Esta regra segue a descrição viva do Dr. Eggbot (fonte de verdade; alinhado em 13/11/2026).
- Só os arquivos sem sufixo `-anterior` valem; os com `-anterior` são backup.

**Por quê:** mantém cada bot igual ao que foi desenhado e aprovado, e evita bots com dois jobs ou sem anti-jobs.

## Modelo padrão

O modelo padrão da fábrica é o grok-4.7 com reasoning_effort high, fast false e context 500k (ver seção 30 de supervisor-operacao-cursor): toda solicitação ao Cursor sem modelo explícito usa esse padrão. Se o humano solicitar um modelo específico no início do fluxo, ele segue em todas as fases até o final. A troca de modelo no meio do fluxo não é automática. Se o grok-4.7 estiver com créditos esgotados, usa outro modelo disponível, nunca o esgotado.

## Regra de ouro de atualização

**Regra de ouro de atualização (decisão do Elienaldo; dono: Mestre de obras):** toda atualização de regra de um bot da fábrica é conduzida pelo Mestre de obras, que no mesmo trabalho atualiza a documentação do projeto (`C:\Users\Elienaldo\Projetos\Fabrica-Agentica`) e a biblioteca correspondente, com backup antes e hash antes/depois. A biblioteca do Supervisor é o conjunto das skills (`supervisor-regras` na camada 1 e as 8 de camada 2; no box, `/home/box/agent-data/workflows`; no PC, o espelho `skills\*.md`). Nos demais bots, a biblioteca é a descrição do bot (bots vivos) e a ficha em `markdown\modelos\` (documentação e fonte dos criados por sessão). Documento e biblioteca não podem ficar com versões diferentes. Vale para todos os trabalhos futuros, sem precisar reescrever cada perfil.

## Economia de contexto (regra 28) vale para todos os bots

Decisao do Elienaldo (12/11/2026): a regra 28 (conversa nova por fase, handoff enxuto, economia de contexto) aplica-se a TODOS os bots da fabrica, sem excecao, inclusive Dr. Eggbot. O Supervisor carrega a regra 28 na skill `supervisor-fases` (camada 2); os demais bots, na descricao (bots vivos) ou na ficha em markdown\modelos\ (criados por sessao), em versoes iguais a documentacao. Nao ha texto canonico unico: cada bot carrega a regra 28 adaptada individualmente na propria ficha em markdown\modelos\ (sem referencias a secoes do Supervisor); no Supervisor, a regra 28 fica em supervisor-fases (camada 2), com as referencias as secoes 2, 15, 26 e 27 que existem so nele. O modelo base foi removido em 13/11/2026.

## Regras do Supervisor em 3 camadas (economia de contexto)
Decisao do Elienaldo em 12/11/2026. A biblioteca de regras do Supervisor e carregada em camadas, nao inteira a cada turno:
- Camada 1 (`supervisor-regras`): nucleo sempre presente, com o essencial, o gatilho de carregamento por fase e o indice dos blocos.
- Camada 2 (8 skills por funcao): `supervisor-fases`, `supervisor-research`, `supervisor-review-merge`, `supervisor-criacao-secao`, `supervisor-destruicao`, `supervisor-operacao-cursor`, `supervisor-comunicacao-humana`, `supervisor-logs` — carregadas so quando o Supervisor assume aquela funcao.
- Camada 3: documentos de fase em `markdown\fases`, anexados sob demanda.
A mensagem de handoff traz o nome da fase e dispara o carregamento das camadas 2 e 3. Biblioteca e documentacao sao mantidas alinhadas (regra de ouro). Nenhum gate, autorizacao ou validacao humana foi removido.

## Dev Expresso avaliado para camadas (12/11/2026)
Dev Expresso avaliado em 12/11/2026: prefixo fixo ~1.692 tokens (descrição viva, 6.766 caracteres; ficha 6.593), sem handoff entre fases, comunicação só com o Supervisor no caminho rápido; decisão: não dividir em camadas, tudo permanece como está.
Principal e Orquestrador: avaliados; por decisão do Elienaldo em 12/11/2026, não divididos em camadas, fichas mantidas como estão.

## Regra 28 adaptada por bot (13/11/2026)
As referências "seção 15", "seção 2" e "seções 26 e 27" foram reescritas sem número em todos os bots, exceto o Supervisor, onde existem. Descrições vivas atualizadas: Dev Expresso, Dr. Eggbot, Grok Bot, Âncora, Mestre de obras. Radar fora da regra 28 (decisão anterior). Principal, Orquestrador, Cirurgião, Curador, Design de front-end, Product Engineer, Advogado do diabo são criados por sessão a partir das fichas (sem bot vivo), então a ficha é a fonte real. Cada ficha carrega sua propria 28 adaptada; o Dr. Eggbot cria o bot a partir da ficha do papel.

## Nome dos grupos (13/11/2026)
Decisão do Elienaldo (13/11/2026, 14:21 Bahia): o grupo de cada fase se chama `<fase>-<nome-da-feature>`, por exemplo `research-feat-nome-da-feature`, com o nome da feature igual ao da seção criada (prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens), gerado automaticamente. Não se usa prefixo `grupo-`. O grupo inicial da feature (antes de qualquer fase) é um só por feature, em qualquer caminho, inclusive no expresso: membros são o Supervisor e o humano que pediu a feature, e o nome é `canal-<nome-da-feature>` (decisão das 14:28 Bahia). Não existe grupo de direção (decisão do Elienaldo, 13/11/2026, 16:55 Bahia): a comunicação é o canal `canal-<nome-da-feature>` e um grupo por fase, `<fase>-<nome-da-feature>`. Regra completa em `markdown\comunicacao.md`, seção 5.
