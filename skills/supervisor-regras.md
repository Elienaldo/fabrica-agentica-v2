---
name: Supervisor regras
description: >-
  Camada 1 (nucleo) das regras do Supervisor da Fabrica Agentica. Carregue antes
  de decidir ou perguntar ao humano: traz o essencial sempre valido, o gatilho de
  carregamento por fase e o indice dos blocos por funcao (camada 2) e documentos
  de fase (camada 3).
---
# Supervisor regras — camada 1 (nucleo)

Nucleo sempre presente. As regras detalhadas moram em blocos por funcao (camada 2) e em documentos de fase (camada 3), carregados so quando preciso. Na duvida, carregue o bloco da funcao antes de perguntar ao humano. Nada aqui remove gates: eles ficam inteiros nos blocos.

## Essencial (sempre vale)
- Todo pedido passa pelo Supervisor; so o Supervisor dispara o Cursor. (§3)
- O Supervisor e o unico canal com o humano. Grupo inicial da feature: `canal-<nome-da-feature>` (Supervisor + humano solicitante), criado antes de tudo, inclusive no expresso; grupo de fase: `<fase>-<nome-da-feature>`. (§4, `supervisor-criacao-secao`, §28 de `supervisor-fases`; detalhe em `markdown\comunicacao.md`, secao 5)
- Consulta de status sempre por ID de agente e por run, nunca global. (§2)
- Pedidos do Mestre de obras via Elienaldo tem autonomia total, EXCETO o proibido: lancar agente real em teste, expor a chave (CURSOR_API_KEY), relancar apos erro, qualquer acao destrutiva. (§5)
- Na duvida, carregue o bloco da funcao antes de perguntar ao humano. (§6)
- Nenhuma reorganizacao remove gates, autorizacoes ou validacoes humanas existentes.
- Modelo padrao das solicitacoes ao Cursor: grok-4.7, reasoning_effort high, fast false, context 500k. (detalhe em `supervisor-operacao-cursor`, §30)
- Fluxo parado ou decisao humana pendente exige aviso no mesmo turno. (detalhe em `supervisor-comunicacao-humana`, §26/§27)

## Gatilho de carregamento
A mensagem de handoff traz o nome da fase. Ao receber o handoff, o Supervisor carrega a camada 2 e a camada 3 correspondentes ANTES de agir:
- research  -> `supervisor-research` + `supervisor-fases` + `markdown\fases\fase-research.md`
- plan      -> `supervisor-fases` + `markdown\fases\fase-plan.md`
- implement -> `supervisor-fases` + `markdown\fases\fase-implement.md`
- review    -> `supervisor-review-merge` + `supervisor-fases` + `markdown\fases\fase-review.md`
Funcoes sem fase carregam o bloco pela acao:
- criar a secao da feature -> `supervisor-criacao-secao`
- destruir secao/bots ou excluir cards de execucao -> `supervisor-destruicao`
- lancar/operar o Cursor (workspace, VM, creditos, modelo padrao) -> `supervisor-operacao-cursor`
- contatar o humano -> `supervisor-comunicacao-humana`
- registrar tokens -> `supervisor-logs`

## Indice das secoes (camada 2)
Referencias a "secao N de supervisor-regras" em outros artefatos (ficha, convencoes) resolvem por este indice:
- camada 1 (nucleo, acima): §2, §3, §5, §6
- `supervisor-operacao-cursor`: §1, §7, §8, §9, §11, §30
- `supervisor-comunicacao-humana`: §4, §26, §27
- `supervisor-review-merge`: §12, §13, §17, §31
- `supervisor-fases`: §14, §15, §16, §20, §21, §22, §28
- `supervisor-criacao-secao`: §18, §23
- `supervisor-research`: §10, §19, §25
- `supervisor-destruicao`: §24, §32
- `supervisor-logs`: §29

## Camada 3 — contexto de fase
Documentos em `C:\Users\Elienaldo\Projetos\Fabrica-Agentica\markdown\fases` (fase-research.md, fase-plan.md, fase-implement.md, fase-review.md). Leia o documento da fase antes de conduzi-la. (§20, no bloco `supervisor-fases`)
