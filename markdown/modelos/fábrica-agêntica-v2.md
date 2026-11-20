# Fábrica agêntica V2

Visão geral e regras comuns da Fábrica Agêntica V2, no estado atual. Cada bot tem a sua ficha em `modelos/` (`bootstrapper.md` e `arquiteto.md`); este documento guarda o que é comum à fábrica: fluxo, regras, limites, política de modelos, skills e ciclo de vida.

Dono do documento: Elienaldo Bittencourt. Redigido pelo Mestre de obras. Adaptado em 15/11/2026 a partir do documento geral da fábrica anterior (`fábrica-agêntica.md`, guardado no backup `Fabrica-Agentica-backups\docs-v1-para-v2-20261115-2225`).

Fontes: `README.md`, as fichas em `modelos/`, as skills `arquiteto-*` e `bootstrapper-*` (espelho em `skills/`) e os documentos de fase em `markdown/fases/`. Em caso de divergência, valem as skills e as fichas.

---

## 1. Visão geral

A fábrica recebe um pedido do humano e entrega código mergeado. Cada feature roda dentro de uma **seção própria** no app, com um único bot: o **Arquiteto** daquela feature.

### Fluxo, em fases

1. **Entrada (Bootstrapper):** recebe o pedido do humano, cria o nome da feature (`feat-...` ou `fix-...`), roda o script de criação de seção (`scripts/criar-secao-feature.py`, que usa o bot **Âncora V2** para abrir a seção nova e depois o devolve à seção Fábrica Agêntica V2), confere a seção pelo nome exato, cria o Arquiteto dentro dela e sai de cena. O Arquiteto não é criado à mão no app: é criado dinamicamente, um por feature. O Bootstrapper não classifica e não fala com o Cursor; mais tarde ele também encerra a feature (item 9).
2. **Avaliação e classificação (Arquiteto):** recebe do Bootstrapper só o pedido original e o nome da feature. Classifica criticidade, risco e complexidade (baixa, média ou alta) e responde às 5 perguntas SIM/NÃO: 1. muda arquitetura? 2. afeta mais de um serviço, ou um componente de que muitos dependem? 3. tem ambiguidade de requisito? 4. é difícil de desfazer (dados persistidos, migração ou quebra de contrato de API)? 5. toca autenticação, permissões, dados pessoais ou segredos? A tag do humano (ex.: "utilize como alta") tem prioridade e dispensa as perguntas. Não há roteamento fixo: o Arquiteto decide começar por research, plan ou implement.
3. **Research:** o Arquiteto acumula as funções de engenharia de produto, design de front-end (protótipo) e advogado do diabo (matriz de objeções). Usa as skills de research (seção 4). Entrevista humana obrigatória quando surgir pergunta que só o humano responde. O OK humano do protótipo é obrigatório antes do plan. Saída: PRD (`tlc-prd`) ou design doc (`tlc-discover`).
4. **Plan:** sessão nova do Cursor com a `tlc-spec-lean` em modo plan (sempre pedir o planejamento e os checks). Artefatos na pasta da feature: `plan.md`, `checks.md`, `verification.md`, `STATE.md` e `LESSONS.md`.
5. **Implement:** sessão nova do Cursor com a `tlc-spec-lean` em modo implement. Teste vermelho é parada e a asserção nunca é enfraquecida. Com tudo verde, o modelo do Cursor faz o push na branch da feature, e o push cria o PR.
6. **Review:** obrigatória antes do merge. Sessão nova do Cursor com a `the-judge` no PR (`--pr <número>`). O Arquiteto gera o resumo visual em HTML para o humano, corrige should fix e nit na sessão da review e leva ao humano blocker, should fix complexo ou com risco e as travas anti-loop.
7. **Merge:** o Arquiteto dispara o merge no GitHub quando a última rodada da the-judge vem limpa e não há blocker pendente (nit pode ficar).
8. **Depois do merge:** ambiente dev, link ao humano e subida só com confirmação explícita do humano. A subida autorizada instala a correção em dev E prod (nunca só em prod). Logo depois de avisar que instalou nos dois, o Arquiteto pergunta ao humano se quer encerrar a feature, sem esperar o pedido; a pergunta não é autorização.
9. **Encerramento da feature:** quando o humano autoriza explicitamente o encerramento, o Arquiteto só avisa o Bootstrapper (handoff com o nome da feature, o id da seção, o id do Arquiteto, os ids e nomes dos grupos o texto e a hora da autorização e o ponteiro `autorizacao_ref` da mensagem do humano: conversa do Arquiteto, posição e hora ISO) e não exclui nada. O Bootstrapper valida pelas travas (remetente = Arquiteto da seção, `ListSections`, dry-run e conferência do ponteiro: ele lê o histórico do Arquiteto e confere que a mensagem existe, é do humano e tem o texto e a hora do handoff) e, sem pedir a confirmação de novo (o humano já autorizou no handoff), roda `scripts/destruir-secao-api.py` inteiro: Arquiteto, seção e grupos. Com qualquer divergência, ou em pedido que não venha desse handoff, para e confirma direto com o humano (autorização repassada por outro bot não vale). Merge ou fim da feature, sozinhos, não autorizam. O Bootstrapper lê o resultado e avisa o humano.

```mermaid
flowchart LR
  H((Humano)) --> B[Bootstrapper: nome da feature]
  B --> S[Script de criação de seção com o Âncora V2]
  S --> B2[Bootstrapper confere a seção e cria o Arquiteto da feature]
  B2 --> C{Arquiteto classifica e decide a fase}
  C --> R[Research]
  C --> P[Plan: tlc-spec-lean]
  C --> I[Implement: tlc-spec-lean]
  R -- OK humano do protótipo --> P
  P --> I
  I -- push cria o PR --> V[Review: the-judge]
  V -- limpa, sem blocker --> M[Arquiteto dispara o merge]
  M --> D[Dev, link ao humano; subida em dev e prod só com confirmação]
  V -. blocker, should fix complexo, 3 rodadas .-> H
  I -. vermelho após 3 rodadas .-> H
  H -- autoriza o encerramento --> A2[Arquiteto avisa o Bootstrapper com o handoff e o ponteiro da autorização]
  A2 --> B3[Bootstrapper valida as travas e confere o ponteiro no histórico do Arquiteto]
  B3 -. divergência: para e pergunta .-> H
  B3 -- travas ok, sem nova pergunta --> X[Bootstrapper roda destruir-secao-api.py: Arquiteto, seção, grupos]
+

+
+  B -. repassa avisos .-> H
  B -. repassa avisos .-> H
```

### Quem é quem

| Bot | Papel | Ficha |
| --- | --- | --- |
| Bootstrapper | Permanente, porta de entrada. Recebe o pedido, cria o nome da feature, roda o script de criação de seção, confere a seção, cria o Arquiteto dentro dela e sai de cena. Recebe o aviso de criação de seção por webhook (rotina "Fábrica V2 — bloqueio criação") e repassa ao humano. No fim da feature, recebe o handoff de encerramento do Arquiteto, valida as travas e roda `destruir-secao-api.py` inteiro (Arquiteto, seção e grupos) sem pedir a confirmação de novo; só pergunta ao humano com divergência ou se o pedido não vier do handoff. Não classifica e não fala com o Cursor. | `bootstrapper.md` |
| Arquiteto | Um por feature, criado dinamicamente pelo Bootstrapper dentro da seção da feature. Único bot da feature: classifica, decide a fase, conduz research, plan, implement e review, opera o Cursor, faz o merge, cuida do dev e da produção com confirmação humana e, com autorização humana explícita de encerramento, só avisa o Bootstrapper (não exclui nada, nem a si mesmo). Faz a comunicação com o humano durante a feature. | `arquiteto.md` |
| Âncora V2 | Permanente, de apoio. Não participa da feature: é o alvo do script de criação de seção, que o move para abrir a seção nova e o devolve à seção Fábrica Agêntica V2. | sem ficha |

**Cursor:** agentes de nuvem que escrevem o código numa VM própria, em branch própria. Só o Arquiteto abre sessão no Cursor; o retorno chega pela notificação de conclusão do agente (`automacoes/comunicacao-bidirecional-cursor.md`).

---

## 2. Regras gerais

### 2.1 Nome da feature e paralelismo

- O nome da feature é o prefixo `feat` ou `fix`, hífen e o nome em minúsculas com hífens (ex.: `feat-nome-da-feature`). É também o nome da seção e a base dos grupos de fase (`<fase>-<nome-da-feature>`).
- A branch de cada pedido segue `feat/` ou `fix/YYYYMMDD-nome-da-task`, nunca a `main`.
- Cada feature tem a sua seção e o seu Arquiteto, então várias features rodam em paralelo sem compartilhar estado.
- Se o nome da feature já existir ativo (seção ou Arquiteto com o mesmo nome), o Bootstrapper recusa a criação e avisa o humano.

### 2.2 Toda fase nova começa com sessão nova

Toda fase nova (research, plan, implement e review) começa com o Arquiteto solicitando ao Cursor uma sessão nova, com contexto limpo, antes de passar qualquer informação. O handoff entre fases passa sempre pelo Arquiteto. Continuações dentro da mesma fase (correção, nova rodada da the-judge, ajuste pedido pelo humano) e o ambiente dev depois do merge seguem na sessão da própria fase.

### 2.3 Research com funções acumuladas

Não há grupo de bots de research. O Arquiteto faz escopo, prioridade e o como técnico, a experiência e o protótipo, e as objeções (matriz de objeções). Nenhuma objeção sem resposta registrada segue para síntese; o que ele não consegue resolver vai ao humano, com as opções.

### 2.4 Skills que faltam

O Arquiteto decide quais skills do fluxo serão usadas e passa essas decisões ao Cursor de forma integral. Ele não instala skills: a instalação, se necessária, é do Cursor.

### 2.5 Limites de rodadas

- Implement: até 3 rodadas de correção na verificação; depois escala ao humano.
- the-judge: máximo de 3 rodadas de revisão por execução; 3 rodadas com blocker param e escalam ao humano.
- Correção dos findings: máximo de 3 rodadas; depois trava e escala ao humano. Should fix gerado 3 vezes seguidas após correções também trava.

### 2.6 Regras para o humano

- **Blocker é sempre humano.** Não se corrige blocker sem autorização humana; com a autorização (e, se houver, a sugestão de correção), a the-judge valida e, se passar, o merge segue sem nova avaliação humana.
- Should fix complexo ou com risco escala ao humano.
- Durante a feature, a comunicação com o humano é do Arquiteto, no grupo da fase. O Bootstrapper só fala com o humano no pedido e nos avisos dos scripts.
- Gates humanos: OK do protótipo antes do plan; review obrigatória antes do merge (bypass só por escrito do humano); produção só com confirmação explícita (a subida vale para dev e prod); nenhum agente real em teste sem o ok do humano; destruição só com autorização explícita de alvo e alcance.

### 2.7 Regra de ouro de atualização

Toda atualização de regra de um bot da fábrica é conduzida pelo **Mestre de obras**, com backup antes, hash antes e depois e releitura do que foi salvo. Skills mudam ao mesmo tempo no box (`/home/box/agent-data/workflows`), no espelho `skills/` da V2 e na descrição do bot no app; fichas e documentação ficam alinhadas.

## 3. Política de modelos

Modelo padrão das solicitações ao Cursor: grok-4.7, reasoning_effort high, fast false, context 500k, quando o pedido não indicar outro. Se o humano pedir um modelo específico no início do fluxo, ele segue em todas as fases. Se o grok-4.7 estiver com créditos esgotados, usa outro modelo disponível, nunca o esgotado.

---

## 4. Skills

Skills não são agentes: são instruções que o modelo do Cursor executa a pedido do Arquiteto. Não há criação ou destruição de skill por feature.

### 4.1 the-judge

- **O que é:** skill de **review de PR**.
- **Quem usa:** o modelo do Cursor, solicitado pelo Arquiteto na fase de review, em sessão nova.
- **Como funciona:** até **3 rodadas** por execução; classifica cada finding em **blocker**, **should fix** ou **nit**. Nova rodada, depois de uma correção, só revisa o diff novo.
- **Saída:** findings, que o Arquiteto transforma no resumo visual para o humano e usa na correção.

### 4.2 TLC Spec Lean

- **O que é:** skill de especificação e execução (nome real: `tlc-spec-lean`).
- **Usos na fábrica:**
  - **Plan:** gera na pasta da feature `plan.md` e `checks.md` (sempre pedir planejamento E checks), além de `verification.md` (reservado), `STATE.md` e `LESSONS.md`.
  - **Implement:** executa o que foi planejado. Os commits, os gates e a verificação são internos da skill.
- **Quem usa:** o modelo do Cursor, disparado pelo Arquiteto. A `tlc-plan` e a `tlc-implement` continuam válidas, mas a `tlc-spec-lean` é a escolha padrão, a menos que o humano diga outra coisa.

### 4.3 grill-me

- **O que é:** skill de **questionamentos** (perguntas duras), para qualquer projeto.
- **Atenção:** pergunta para o humano interrompe a research até a resposta real ser registrada.

### 4.4 wayfinder

- **O que é:** skill de mapa de decisões, opcional, **só para início de projeto**; convive com o grill-me, e um não substitui o outro.
- **Quem decide:** o Arquiteto; se ele não conseguir decidir, pergunta ao humano.

### 4.5 prototype

- **O que é:** skill de **protótipo descartável**, que nunca vira código de produção.
- **Quando usa:** dúvida visual ou de interação: feature nova, mudança grande de front-end ou pedido do humano. O OK do humano ao protótipo é obrigatório antes do plan.

### 4.6 tlc-discover

- **O que é:** skill do Tech Leads Club que conduz uma **entrevista** e gera um **design document**, em `.design/<nome>.md` (situação, problema, sucesso, fronteira, forma, decisões-chave e trabalho em fatias).
- **Observação:** se o risco for baixo, ela responde num parágrafo e não gera arquivo.

### 4.7 tlc-prd

- **O que é:** skill do Tech Leads Club que conduz uma **entrevista** e gera um **PRD**, em `.prd/<slug>.md` (situação, problema, sucesso, fronteira e tabela de journey). Para antes de qualquer design técnico.
- **to-spec:** fora da fábrica, por ser redundante com a tlc-prd.

---

## 5. Ciclo de vida

| Momento | Quem faz | O quê |
| --- | --- | --- |
| Pedido chega | Bootstrapper | Cria o nome da feature e roda o script de criação de seção. |
| Criação | Bootstrapper | Confere a seção pelo nome exato e cria nela o Arquiteto exclusivo da feature; entrega ao humano o nome da feature, a confirmação da seção e o ID do Arquiteto; sai de cena. |
| Execução | Arquiteto | Conduz as fases, cada uma com sessão nova do Cursor e grupo `<fase>-<nome-da-feature>` só com ele e o humano. |
| Merge | Arquiteto | Dispara o merge com a review limpa e sem blocker pendente. |
| Depois do merge | Arquiteto | Dev, link ao humano; subida só com confirmação explícita, instalada em dev e prod; logo depois, pergunta ao humano se quer encerrar a feature (a pergunta não é autorização). |
| Encerramento da feature (destruição) | Bootstrapper, por `scripts/destruir-secao-api.py`, depois do aviso do Arquiteto | Com a autorização do humano que vem no handoff do próprio Arquiteto da seção, depois de passar nas travas (remetente, `ListSections`, dry-run, ponteiro da autorização conferido no histórico do Arquiteto); fora do handoff, ou com qualquer divergência, só com a confirmação direta do humano ao Bootstrapper (alvo e alcance). A autorização repassada por outro bot não vale. Ordem: Arquiteto, seção e grupos `<fase>-<feature>` (grupos só com `--confirmar-grupos`). Sem `--executar`, só planeja. O Bootstrapper é protegido. |
| Avisos dos scripts | Bootstrapper | Recebe por webhook o aviso de criação e repassa ao humano. O script de destruição não envia webhook: o Bootstrapper lê o resultado e avisa o humano. Não corrige, não reexecuta e não decide. |

## 28. Conversa nova por fase e handoff enxuto (economia de contexto)
Decisão do Elienaldo em 11/11/2026. Cada fase abre uma conversa, grupo ou sessão nova; o handoff leva só a decisão tomada e o link ou caminho do artefato; evita-se vaivém de status; com os agentes do Cursor, o pedido completo vai só na abertura da sessão da fase; confirmação de sim ou não em uma frase. Texto completo em cada ficha (`modelos/arquiteto.md`, `modelos/bootstrapper.md`) e na skill `arquiteto-fases`. A regra não remove gates, autorizações nem validações humanas.
