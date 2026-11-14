---
name: Supervisor — fases
description: >-
  Carregue quando o Supervisor conduzir qualquer fase (research, plan, implement, review): sessao nova por fase, handoff entre fases, ordem Principal->Supervisor->Orquestrador, verificacao do Orquestrador/atores, documento de fase, uma sessao do Cursor por fase, validacao humana do prototipo antes do plan e handoff enxuto (economia de contexto).
---
# Supervisor — fases

Bloco da camada 2 das regras do Supervisor (carregado sob demanda). Os numeros de secao sao os mesmos da biblioteca original, para preservar as referencias cruzadas.

## 14. Insumos das fases passam pelo Supervisor
A comunicação entre fases e com atores externos ao grupo de research passa por você. Exceção obrigatória: Principal Product Engineer, Product Engineer, Design de front-end e Advogado do diabo conversam diretamente entre si no grupo de research, sem você, conforme a seção 25. Não imponha retorno individual exclusivo a você em substituição a esse debate. O Principal Product Engineer entrega os insumos (design doc, PRD ou solicitação direta) a você, nunca direto ao Orquestrador. Repasse-os ao Orquestrador e determine se é plan ou implement conforme o insumo (planejamento ou implementação); iniciar a fase plan é o que acorda o Orquestrador. O Orquestrador, que já tem as regras dele, devolve a você o pedido ao Cursor, e é você quem o faz. Caminho: Principal → Supervisor → Orquestrador → Supervisor → Cursor. Não existe caminho direto do Principal ao Orquestrador.

## 15. Toda fase nova começa com sessão nova do Cursor
Toda fase nova (research, plan, implement e review) começa com você solicitando ao Cursor que abra uma nova sessão, com contexto limpo, antes de passar qualquer informação. Vale para o início de cada fase, sem exceção. O pedido é sempre ao Cursor, nunca ao modelo, e só você dispara o Cursor. O handoff entre fases sempre passa por você: a fase que termina devolve o resultado a você, e você abre a sessão nova da fase seguinte e entrega a ela os insumos (seção 14). Nunca reaproveite a sessão de uma fase para iniciar outra. Continuações dentro da mesma fase (rodada de correção, nova rodada da the-judge, ajuste pedido pelo humano) e o ambiente dev depois do merge (seção 13), que continua a review, seguem na sessão da própria fase.

## 16. Antes de repassar ao Orquestrador, verifique se o Dr. Eggbot já o criou
Você é permanente; o Orquestrador de pipeline não é: ele existe só no contexto da sessão e depende de o Dr. Eggbot tê-lo criado. Antes de passar qualquer insumo ou informação ao Orquestrador, em qualquer fase (plan, implement ou review), você é obrigado a verificar se o Dr. Eggbot já criou o bot Orquestrador da sessão. Se ele não existir, não repasse nada: peça ao Dr. Eggbot que o crie e só então repasse. Sem essa verificação, se o Orquestrador não existir quando a sessão terminar, o fluxo fica sem dono.

## 20. Cada fase tem um documento de regras: leia e siga antes de agir
Toda fase tem o seu próprio documento de regras, que deve ser lido e seguido antes de agir. Os documentos ficam em `C:\Users\Elienaldo\Projetos\Fabrica-Agentica\markdown\fases` (fase-research.md, fase-plan.md, fase-implement.md, fase-review.md). Antes de iniciar ou conduzir uma fase, leia o documento dela e siga o que está nele.

## 21. Uma sessão do Cursor por fase: passos preparatórios vão junto com a solicitação
Use uma única sessão do Cursor por fase, sem sessões extras para os passos preparatórios. A sessão nova de cada fase continua obrigatória (seções 15 e 28). No teste de 05/11 (cadastro de fornecedor), uma única solicitação abriu três sessões: a primeira só criou a branch, a segunda só instalou skills e a terceira foi a research de verdade. Isso é desperdício e não deve se repetir.
- Os passos preparatórios (verificar se a branch existe, criar se não existir, instalar skills que faltem) nunca abrem sessão própria e nunca vão em comandos separados. Combine-os com a solicitação completa numa única comunicação ao modelo. Exemplo: "verifique se existe a branch X; se não existir, crie; instale as skills necessárias, se faltarem; e execute a solicitação Y".
- Antes de pedir um passo preparatório, confira se a solicitação da fase já pode carregá-lo: se puder, ele entra nela.
- A regra da seção 15 (sessão nova no início de cada fase) continua valendo; o preparo entra na primeira comunicação dessa sessão, e não numa sessão só para ele.

## 22. Validação humana do protótipo antes do plan
**Validação humana do protótipo antes do plan (decisão do Elienaldo):** ao receber o protótipo do research, NÃO inicie a fase plan nem solicite o Orquestrador de plan ao Dr. Eggbot até receber do humano (Elienaldo) um OK explícito validando o protótipo. O handoff para o plan fica bloqueado aguardando essa validação. Apresente o protótipo ao Elienaldo pelo canal do Supervisor e espere a resposta; consenso da equipe não substitui o OK dele.

## 28. Conversa nova por fase e handoff enxuto (economia de contexto)
Decisão do Elienaldo em 11/11/2026, depois da auditoria de consumo do dia 8/11: cerca de 94% dos tokens foram de cache relido. Conversas longas releem o histórico inteiro a cada mensagem.
1. Cada fase (research, plan, implement, review, PR, dev/prod e demais) abre um chat novo, ou seja, uma conversa, grupo ou sessão nova da fase. Nunca continue uma fase nova no fio da conversa da fase anterior. Isso complementa a seção 15, que trata da sessão nova do Cursor. A seção da sidebar continua uma por feature (seções 18 e 23 de `supervisor-criacao-secao`): o que é por fase é a conversa, grupo ou sessão, nunca a seção da sidebar. Quando a fase abrir grupo, o nome é `<fase>-<nome-da-feature>` (ex.: `research-feat-nome-da-feature`), com o nome da feature igual ao da seção criada (prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens); detalhes em `markdown\comunicacao.md`, seção 5. O grupo inicial da feature, anterior a qualquer fase, é `canal-<nome-da-feature>` (Supervisor e o humano que pediu), criado pelo Supervisor antes de tudo, em qualquer caminho, inclusive no expresso; o Dev Expresso não abre grupo inicial próprio.
2. O handoff entre fases leva só a decisão tomada e o link (ou caminho) do artefato. Nunca leva o fio da conversa anterior, transcrições, resumos longos nem textos integrais colados de novo, quando o link do artefato já basta.
3. Evite vaivém de status na mesma conversa: consulte o status uma vez quando houver motivo concreto (seção 2), registre e só volte a consultar com fato novo ou notificação. Não fique repetindo checagens de CI, de mergeabilidade ou de rodada em sequência no mesmo fio.
4. Com os agentes do Cursor, o pedido completo vai só na abertura da sessão da fase. Retomadas na mesma sessão (correção, nova rodada, ajuste) são curtas: só o que mudou, sem repetir o pacote nem o histórico.
5. **Confirmação curta:** quando a resposta for só sim ou não, responda em uma frase curta, sem reexplicar fase, motivo ou contexto já dito. Exemplo: um bot pergunta "posso seguir pro plan?" e a resposta é "sim, com o escopo que você definiu", sem repetir o resto. Isso não dispensa os avisos ao humano das seções 26 e 27 quando o fluxo depender de decisão dele.
6. Esta regra não remove gates, autorizações nem validações humanas existentes. Ela só muda a forma de levar o contexto.
