# Comunicação da fábrica

**Nome:** Comunicação da fábrica

**Responsável:** Dr. Eggbot. Quem lê este documento e cria sessões é ele.

> **OBRIGATÓRIO:** não existe grupo de direção. A comunicação da feature é: (1) o canal `canal-<nome-da-feature>`, entre o Supervisor e o humano que pediu, criado pelo Supervisor antes de tudo; (2) um grupo por fase, `<fase>-<nome-da-feature>`, aberto quando a fase começa — não na criação da sessão. O grupo **research** nasce junto com os agentes de research, quando o Principal classifica a feature como SIM. O grupo **review** não é criado com a sessão: abre quando a fase review começa, como os demais grupos de fase. Isso é permissão fixa dada pelo Elienaldo: vale para toda feature, sem exceção, e o Dr. Eggbot não espera pedido do humano a cada feature para criar o grupo da fase que lhe cabe. Feature sem o canal inicial, ou fase sem o seu grupo, não está pronta.

**Job único:** definir quem fala com quem, em quais grupos do Grok Bot, por onde tudo passa e como os grupos nascem, encerram e são apagados. Os papéis e as fases estão em `fábrica-agêntica.md`.

**Anti-jobs:** o Dr. Eggbot nunca deixa de criar o grupo da fase que lhe cabe; nunca espera pedido do humano para criar esses grupos; nunca reaproveita canal entre features; nunca apaga canal (não consegue); nunca coloca o Cursor em grupo; nunca deixa um bot falar com o humano fora do Supervisor; nunca cria grupo de direção.

**Voz:** regra imperativa, sem exceção.

**Acordar:** sob demanda, quando o Supervisor pede a criação de uma sessão. A destruição da seção não é iniciada pelo Dr. Eggbot: o Supervisor inicia o script local somente com autorização explícita de alvo/escopo e capacidades validadas, conforme a seção 24 de supervisor-destruicao.

## 1. Criação dos grupos (permissão fixa)

1. O Supervisor cria, antes de tudo, o canal `canal-<nome-da-feature>` (ele e o humano que pediu a feature).
2. O grupo permanente (Supervisor e Dr. Eggbot) existe antes de qualquer sessão e não é recriado a cada feature.
3. O grupo de research nasce quando o Principal classifica a feature como SIM para research e o Dr. Eggbot cria os agentes de research. Se a feature pega o atalho, não existe grupo de research.
4. Os demais grupos de fase (`plan-`, `implement-`, `review-` e outros) abrem quando a fase começa, não na criação da sessão. O grupo de review, portanto, não é criado com a sessão.
5. Cada grupo é um canal do Grok Bot com no máximo 6 membros. Canais não se aninham.
6. O Dr. Eggbot cria canais e muda membros. Não esvazia canal (sempre sobra pelo menos 1 membro) e não apaga canal. Só o humano apaga, pela barra lateral.
7. Não existe grupo de direção. O que antes passava por ele (Supervisor↔Principal, Supervisor↔Orquestrador, entrega de insumos, pedidos ao Cursor, falhas e escaladas) acontece no grupo da fase em curso.

## 2. Grupos

| Grupo | Membros (agentes) | Quando existe |
|---|---|---|
| Permanente | Supervisor e Dr. Eggbot (o humano acompanha) | Sempre |
| Canal da feature (`canal-<nome-da-feature>`) | Supervisor e o humano que pediu | Toda feature, criado pelo Supervisor antes de tudo |
| Research (`research-<nome-da-feature>`) | Principal Product Engineer, Product Engineer, Design de front-end e Advogado do diabo | Só quando o Principal classificar a feature como SIM para research; aberto com os agentes de research |
| Plan / implement / review (`<fase>-<nome-da-feature>`) | Supervisor, Orquestrador de pipeline e os bots da fase (na review: Cirurgião e Curador amigável) | Aberto quando a fase começa, não com a sessão |

O Supervisor entra nos grupos de fase plan, implement e review. Não entra no de research: o debate dos quatro permanece sem ele. A entrega de insumos e o resultado do research passam pelo Principal; não há grupo de direção.

## 3. Pares de comunicação

| Par | Onde acontece |
|---|---|
| Supervisor e humano (Elienaldo) | Canal `canal-<nome-da-feature>` |
| Supervisor e Dr. Eggbot | Grupo permanente |
| Supervisor e Principal | Grupo da fase em curso (no research: entrega de insumos e resultado ao Principal; o debate dos quatro permanece no grupo de research, sem o Supervisor) |
| Principal e Orquestrador | **Não se falam direto**: o Principal entrega os insumos ao Supervisor, que os repassa ao Orquestrador (grupo da fase em curso) |
| Orquestrador e Supervisor (insumos recebidos, pedidos ao Cursor, falhas e escaladas) | Grupo da fase em curso |
| Principal, Product Engineer, Design de front-end e Advogado do diabo | Grupo de research |
| Orquestrador, Cirurgião e Curador (com o Supervisor) | Grupo de review |
| Principal e sessões do Cursor (fase research) | **Fora do Grok Bot**: o Cursor não é agente do Grok Bot, então não entra em grupo |
| Orquestrador e sessões do Cursor (fases plan, implement e review) | **Fora do Grok Bot**, pelo mesmo motivo |

## 4. Roteamento

1. Tudo que vai para o humano passa pelo Supervisor, sem exceção.
2. O Curador entrega HTML e documentos ao Supervisor, que os repassa ao humano.
3. A decisão do humano volta pelo mesmo caminho: humano, Supervisor, grupo em que a pergunta nasceu.
4. Quem fala com o Cursor: só o Supervisor. Nas fases plan, implement e review, o Orquestrador pede ao Supervisor que dispare; na fase research, o Principal pede ao Supervisor que dispare. Nas demais fases o Supervisor posta o resumo do resultado no grupo da fase; no research, entrega os insumos ao Principal, e o Principal os compartilha no grupo dos quatro e conduz a conversa, sem incluir o Supervisor nele.
5. A comunicação entre fases e com atores externos ao grupo de research passa pelo Supervisor. Exceção obrigatória: os quatro atores conversam diretamente entre si no grupo de research, sem Supervisor; não se exige retorno individual exclusivo a ele em substituição ao debate. O Principal entrega os insumos (design doc, PRD ou solicitação direta) ao Supervisor; o Supervisor os repassa ao Orquestrador e determina se é plan ou implement; o Orquestrador devolve ao Supervisor o pedido ao Cursor, e o Supervisor o faz (Principal → Supervisor → Orquestrador → Supervisor → Cursor). Não existe caminho direto do Principal ao Orquestrador. A conversa interna do time de research, no grupo de research (onde o Supervisor não entra), é da própria fase.
6. Toda fase nova (research, plan, implement e review) começa com o Supervisor solicitando ao Cursor que abra uma nova sessão, com contexto limpo, sem exceção. O handoff entre fases passa sempre pelo Supervisor, que dispara a sessão nova. Nenhuma fase reaproveita a sessão da anterior.

## 5. Nome dos canais e encerramento

1. Nome padronizado do grupo de fase (decisão do Elienaldo, 13/11/2026): `<fase>-<nome-da-feature>`, por exemplo `research-feat-nome-da-feature` ou `review-feat-nome-da-feature`. O nome da feature é o mesmo que ela recebe ao ser criada, isto é, o nome da seção (seção 18 de `supervisor-criacao-secao`: prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens). Vale para o grupo de research, o de review e o grupo de qualquer outra fase.
   - O grupo inicial da feature (antes de qualquer fase) é um só por feature, em qualquer caminho, inclusive no expresso, porque a comunicação é sempre com o Supervisor, canal único com o humano. Membros: o Supervisor e o humano que pediu a feature. Nome: `canal-<nome-da-feature>`, por exemplo `canal-feat-nome-da-feature`.
   - Formato anterior dos grupos de fase, substituído em 13/11/2026: `feat-<slug>-AAAAMMDD.<tipo>` (tipo `research` ou `review`).
2. Ao encerrar uma feature, cada grupo recebe uma mensagem final em maiúsculas, com o link do registro de decisões.
3. Em seguida os bots saem do canal, deixando um membro. Assim não recebem mais nada.
4. Canal nunca é reaproveitado entre features, porque mistura contexto.

## 6. Histórico

1. O canal fica arquivado por 30 dias. O humano apaga em lote ou na hora, como preferir.
2. A conversa do canal não vale como histórico. O registro de verdade é a documentação do projeto: ADRs, lições e estado das skills.
3. No ADR existente, acrescenta-se uma única linha com o veredito final da revisão: passou ou não.

**Como concreto:** canais do Grok Bot (criar canal e mudar membros). Nenhuma skill da fábrica.

**Ciclo de vida:** permanente; vale para toda sessão.

## 7. Pontos em aberto (a confirmar com o Elienaldo)

- **Prefixo:** o ditado dizia `fit`; foi gravado `feat`, para casar com a sessão `feat/`. Confirmar.
- **Dono do ADR:** quem escreve a linha do veredito não está definido.
- **Abertura e fechamento:** no research, o Principal abre a rodada após instrução do Supervisor e registra o fechamento/resultado; a abertura e a mensagem final dos demais grupos continuam sem dono definido aqui.

## 8. Entrega e abertura do research — regra operacional

Este requisito se aplica somente à equipe de research; não se aplica a equipes de plan, implement, review ou de outros tipos. Preserve as regras já existentes dos demais grupos.

1. Ao formar research autorizado para a feature, o Dr. Eggbot cria OU confirma seu canal com EXATAMENTE Principal Product Engineer, Product Engineer, Design de front-end e Advogado do diabo. Supervisor e Cursor ficam fora. A permissão fixa dispensa nova aprovação humana, mas não autoriza agir em canal de outra feature nem alterar membros de modo inseguro.
2. O Dr. Eggbot devolve ao Supervisor identificação do pedido/feature/seção, os quatro IDs, `group_id` e lista de membros confirmada. Grupo errado/ambíguo/extra/ausente significa entrega parcial bloqueada e divergência evidenciada, não equipe completa. Não basta devolver IDs de bots. O Supervisor confere; nenhum dos dois infere membros apenas pelo nome do canal.
3. Ao receber documentação/inspeção de research com o grupo pronto e entrevista obrigatória resolvida, o Supervisor instrui o Principal, no mesmo turno, a compartilhar os insumos e iniciar o brainstorm no grupo dos quatro. Não pede ao humano se pode iniciar a conversa. O Principal é dono da abertura, condução e registro; o Supervisor recebe o resultado do Principal.
4. Os quatro discutem diretamente no canal; essa conversa interna é exceção expressa ao roteamento transversal pelo Supervisor. Não substitua a rodada por coleta individual exclusiva do Supervisor. O Principal mantém matriz de todas as objeções, respostas nominais, evidências/limites, avaliação do Advogado, decisão ou estado pendente/resolvida e motivo. Incluem-se as seis objeções de Fornecedores e quaisquer outras. Os três votantes registram posição e respostas; o Advogado confronta sem votar, decidir ou propor solução.
5. Nenhuma objeção sem resposta registrada segue para síntese. Exija consenso explícito de Principal, Product e Design, de mesmo peso; após até duas rodadas sem consenso, o Principal escala o impasse ao Supervisor, que busca decisão humana e a registra com os ajustes necessários. Não trate encaminhamento de objeções, silêncio ou votos condicionais como fase concluída.
6. Perguntas humanas obrigatórias de requisito interrompem a rodada quando necessárias, pelo Supervisor, mesmo antes do limite de rodadas. Siga o bloqueio de entrevista de `fases/fase-research.md`. O OK humano do protótipo antes de PLAN permanece obrigatório. Abertura ordinária não requer autorização adicional; isso não elimina esses gates humanos.
7. Registre uma abertura por pedido/versão de insumos; continuações não recriam equipe nem reiniciam o fluxo. Trata-se de instrução sob demanda, não rotina/webhook/listener novo. A regra detalhada do Supervisor é a seção 25 de `../skills/supervisor-research.md`.
