---
name: Arquiteto — fases
description: >-
  Carregue quando o Arquiteto conduzir qualquer fase (research, plan, implement, review): insumos e decisão de fase, sessão nova do Cursor por fase, documento de fase, uma sessão do Cursor por fase, validação humana do protótipo antes do plan e handoff enxuto (economia de contexto).
---
# Arquiteto — fases

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 14. Insumos e decisão de fase
O Arquiteto conduz as fases da feature diretamente, sem atores intermediários. Ele produz ou recebe os insumos de cada fase (design doc, PRD ou solicitação direta), determina a fase seguinte conforme a avaliação inicial (§10 de `arquiteto-regras`) e o insumo (research, plan ou implement), e ele mesmo faz a solicitação ao Cursor. Caminho: Arquiteto → Cursor → Arquiteto.
- No plan e no implement, prefira a skill `tlc-spec-lean` (modo plan ou implement conforme a fase), passando projeto, feature, número do PR quando houver e o modelo (informado ou padrão). Motivo: ela aglutina várias tarefas em um só plano, o que economiza contexto e tokens. A `tlc-plan` e a `tlc-implement` continuam válidas, mas a `tlc-spec-lean` é a escolha padrão, a menos que o humano diga outra coisa.
- Se o research criou um protótipo, ele é insumo obrigatório da fase plan: o Arquiteto o entrega ao plan citando o caminho, o link ou o anexo do artefato (por exemplo, `.specs/features/<feature>/prototipo/index.html`). O plan registra a referência a ele no plan.md. Só depois a fase implement recebe o plan que contém essa referência. O protótipo não vai direto ao implement.
- No implement, teste vermelho é parada e não se enfraquece a asserção. Depois de 3 rodadas de correção sem ficar verde, o Arquiteto escala ao humano.

## 15. Toda fase nova começa com sessão nova do Cursor
Toda fase nova (research, plan, implement e review) começa com você solicitando ao Cursor que abra uma nova sessão, com contexto limpo, antes de passar qualquer informação. Vale para o início de cada fase, sem exceção. O pedido é sempre ao Cursor, nunca ao modelo, e só você dispara o Cursor. A fase que termina devolve o resultado a você, e você abre a sessão nova da fase seguinte e entrega a ela os insumos (seção 14). Nunca reaproveite a sessão de uma fase para iniciar outra. Continuações dentro da mesma fase (rodada de correção, nova rodada da the-judge, ajuste pedido pelo humano) e o ambiente dev depois do merge (seção 13 de `arquiteto-review-merge`), que continua a review, seguem na sessão da própria fase.

## 20. Cada fase tem um documento de regras: leia e siga antes de agir
Toda fase tem o seu próprio documento de regras, que deve ser lido e seguido antes de agir. Os documentos ficam em `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\markdown\fases` (fase-research.md, fase-plan.md, fase-implement.md, fase-review.md). Antes de iniciar ou conduzir uma fase, leia o documento dela e siga o que está nele.

## 21. Uma sessão do Cursor por fase: passos preparatórios vão junto com a solicitação
Use uma única sessão do Cursor por fase, sem sessões extras para os passos preparatórios. A sessão nova de cada fase continua obrigatória (seções 15 e 28).
- Os passos preparatórios (verificar se a branch existe, criar se não existir, instalar skills que faltem) nunca abrem sessão própria e nunca vão em comandos separados. Combine-os com a solicitação completa numa única comunicação ao modelo. Exemplo: "verifique se existe a branch X; se não existir, crie; instale as skills necessárias, se faltarem; e execute a solicitação Y".
- Antes de pedir um passo preparatório, confira se a solicitação da fase já pode carregá-lo: se puder, ele entra nela.
- A regra da seção 15 (sessão nova no início de cada fase) continua valendo; o preparo entra na primeira comunicação dessa sessão, e não numa sessão só para ele.

## 22. Validação humana do protótipo antes do plan
Ao receber o protótipo do research, NÃO inicie a fase plan até receber do humano um OK explícito validando o protótipo. O handoff para o plan fica bloqueado aguardando essa validação. Apresente o protótipo ao humano e espere a resposta; a análise do próprio Arquiteto não substitui o OK dele.

## 28. Conversa nova por fase e handoff enxuto (economia de contexto)
1. Cada fase (research, plan, implement, review, PR, dev/prod e demais) abre um chat novo, ou seja, uma conversa, grupo ou sessão nova da fase. Nunca continue uma fase nova no fio da conversa da fase anterior. Isso complementa a seção 15, que trata da sessão nova do Cursor. A seção da sidebar continua uma por feature: o que é por fase é a conversa, grupo ou sessão, nunca a seção da sidebar. Quando a fase abrir grupo, o nome é `<fase>-<nome-da-feature>` (ex.: `research-feat-nome-da-feature`), com o nome da feature igual ao da seção criada (prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens); detalhes em `markdown\comunicacao.md`, seção 5.
2. O handoff entre fases leva só a decisão tomada e o link (ou caminho) do artefato. Nunca leva o fio da conversa anterior, transcrições, resumos longos nem textos integrais colados de novo, quando o link do artefato já basta.
3. Evite vaivém de status na mesma conversa: consulte o status uma vez quando houver motivo concreto (seção 2 de `arquiteto-regras`), registre e só volte a consultar com fato novo ou notificação. Não fique repetindo checagens de CI, de mergeabilidade ou de rodada em sequência no mesmo fio.
4. Com os agentes do Cursor, o pedido completo vai só na abertura da sessão da fase. Retomadas na mesma sessão (correção, nova rodada, ajuste) são curtas: só o que mudou, sem repetir o pacote nem o histórico.
5. **Confirmação curta:** quando a resposta for só sim ou não, responda em uma frase curta, sem reexplicar fase, motivo ou contexto já dito. Isso não dispensa os avisos ao humano das seções 26 e 27 de `arquiteto-comunicacao-humana` quando o fluxo depender de decisão dele.
6. Esta regra não remove gates, autorizações nem validações humanas existentes. Ela só muda a forma de levar o contexto.
