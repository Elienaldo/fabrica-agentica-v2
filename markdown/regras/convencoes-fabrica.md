# Convenções da fábrica agêntica

**Data:** 2026-11-02 · **Adaptado para a V2:** 2026-11-15

## Branches

Toda nova solicitação cria uma branch nova. Nunca se reutiliza branch de outra solicitação.

**Padrão de nome:** `feat/YYYYMMDD-nome-da-task`

- `feat` é a abreviação de feature.
- `YYYYMMDD` é ano, mês e dia.
- `nome-da-task` é o slug gerado automaticamente pelo Arquiteto a partir das palavras principais da solicitação, sem artigos e preposições, com até uns três termos e hífen entre eles. O slug é o mesmo nome da task.

**Exemplo:** `feat/20261102-botao-login`

**Por quê:** isola uma solicitação da outra e deixa o merge limpo.

## Campos que a notificação de conclusão não traz

A notificação de conclusão do agente de nuvem não traz o campo tipo nem o slug de origem. Os dois vêm do Arquiteto, que os registra no livro-razão ao lançar o agente e os recupera pelo ID do agente. Quem preenche esses campos é o Arquiteto, não o agente que roda. Não há webhook no fluxo.

## Criação de bots: sempre pelo modelo

Na V2, o único bot criado pela fábrica é o Arquiteto, e quem cria é o Bootstrapper. O Arquiteto não é criado à mão no app: é criado dinamicamente, um por feature. O Bootstrapper recebe a feature, roda o script que cria a seção com o nome da feature e, com a seção confirmada, cria o Arquiteto exclusivo daquela feature dentro dela.

- O modelo do Arquiteto é a ficha `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\markdown\modelos\arquiteto.md`: nome, job, anti-jobs, voz, quando acorda e como concreto. O Bootstrapper não cria o Arquiteto de cabeça nem a partir de descrição solta no pedido.
- Se o pedido contradisser a ficha, vale a ficha; a divergência vai ao Elienaldo antes de criar.
- Passos e limites da criação: skills `bootstrapper-start` e `bootstrapper-criacao-arquiteto`. Encerramento da feature: skill `bootstrapper-encerramento`.

**Por quê:** mantém cada Arquiteto igual ao que foi desenhado e aprovado.

## Modelo padrão

O modelo padrão da fábrica é o grok-4.7 com reasoning_effort high, fast false e context 500k (ver seção 30 de arquiteto-operacao-cursor): toda solicitação ao Cursor sem modelo explícito usa esse padrão. Se o humano solicitar um modelo específico no início do fluxo, ele segue em todas as fases até o final. A troca de modelo no meio do fluxo não é automática. Se o grok-4.7 estiver com créditos esgotados, usa outro modelo disponível, nunca o esgotado.

## Regra de ouro de atualização

**Regra de ouro de atualização (decisão do Elienaldo; dono: Mestre de obras):** toda atualização de regra de um bot da fábrica é conduzida pelo Mestre de obras, que no mesmo trabalho atualiza a documentação do projeto (`C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2`) e a biblioteca correspondente, com backup antes e hash antes/depois. A biblioteca do Arquiteto é o conjunto das skills (`arquiteto-regras` na camada 1 e as 7 de camada 2; no box, `/home/box/agent-data/workflows/arquiteto-*`; no PC, o espelho `skills\arquiteto-*.md`). No Bootstrapper, a biblioteca são as skills `bootstrapper-*` (box e espelho `skills\`), a descrição do bot no app e a ficha `markdown\modelos\bootstrapper.md`. Documento e biblioteca não podem ficar com versões diferentes. Vale para todos os trabalhos futuros, sem precisar reescrever cada perfil.

## Economia de contexto (regra 28) vale para todos os bots

Decisão do Elienaldo (12/11/2026): a regra 28 (conversa nova por fase, handoff enxuto, economia de contexto) aplica-se a todos os bots da fábrica, sem exceção. O Arquiteto carrega a regra 28 na skill `arquiteto-fases` (camada 2) e na ficha `markdown\modelos\arquiteto.md`; o Bootstrapper, na ficha `markdown\modelos\bootstrapper.md`, adaptada a ele. Não há texto canônico único: cada ficha carrega a sua versão.

## Regras do Arquiteto em 3 camadas (economia de contexto)
Decisao do Elienaldo em 12/11/2026. A biblioteca de regras do Arquiteto e carregada em camadas, nao inteira a cada turno:
- Camada 1 (`arquiteto-regras`): nucleo sempre presente, com o essencial, o gatilho de carregamento por fase e o indice dos blocos.
- Camada 2 (7 skills por funcao): `arquiteto-fases`, `arquiteto-research`, `arquiteto-review-merge`, `arquiteto-destruicao` (aviso de encerramento ao Bootstrapper), `arquiteto-operacao-cursor`, `arquiteto-comunicacao-humana`, `arquiteto-logs` — carregadas so quando o Arquiteto assume aquela funcao.
- Camada 3: documentos de fase em `markdown\fases`, anexados sob demanda.
A mensagem de handoff traz o nome da fase e dispara o carregamento das camadas 2 e 3. Biblioteca e documentacao sao mantidas alinhadas (regra de ouro). Nenhum gate, autorizacao ou validacao humana foi removido.

## Nome dos grupos (13/11/2026)
Decisão do Elienaldo (13/11/2026, 14:21 Bahia): o grupo de cada fase se chama `<fase>-<nome-da-feature>`, por exemplo `research-feat-nome-da-feature`, com o nome da feature igual ao da seção criada (prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens), gerado automaticamente. Não se usa prefixo `grupo-`. Não existe grupo inicial nem grupo de direção: a comunicação é um grupo por fase, criado pelo Arquiteto, só com ele e o humano. Regra completa em `markdown\comunicacao.md`, seção 5.
