# Comunicação bidirecional Grok Bot e Cursor

**Data:** 2026-11-04 · **Adaptado para a V2:** 2026-11-15
**Status:** validado de ponta a ponta na fábrica anterior, no teste real `req-20261103-001`. Na V2 o ator é o Arquiteto; o fluxo ainda não foi testado de verdade com ele.
**Canal oficial de retorno:** a notificação de conclusão do agente de nuvem. O webhook do Cursor **não é usado** na fábrica.

## 1. Resumo

- **Ida:** só o Arquiteto lança agentes no Cursor, pela API v1 de agentes (ele usa a ferramenta de agente de nuvem do Cursor, que já tem a chave).
- **Volta:** o retorno chega ao Arquiteto como **notificação de conclusão do agente de nuvem**, que acorda o próprio Arquiteto. Esse é o canal oficial.
- **Casamento:** o Arquiteto grava o ID do agente no livro-razão ao lançar e cruza esse ID quando a notificação chega.
- **Webhook:** não é usado e não é necessário. A API v1 não tem webhook. Nada no fluxo depende dele.

## 2. Fluxo completo, passo a passo

1. O Arquiteto resolve o workspace do projeto e confere as regras (skill `arquiteto-operacao-cursor`: modelo com créditos esgotados, política de VM etc.).
2. O Arquiteto lança o agente no Cursor, informando repositório, título e prompt. O título segue o padrão `slug-fase-request_id`. O prompt manda trabalhar numa branch padronizada com data, por solicitação (`feat/` ou `fix/YYYYMMDD-nome-da-task`), nunca na `main`.
3. O Cursor devolve o **ID do agente** (`bc-…`). O Arquiteto grava no livro-razão, junto do pedido: `request_id`, slug, fase e **ID do agente**. Sem essa gravação não há casamento.
4. O agente trabalha na VM do Cursor.
5. Quando o agente termina, o Cursor envia a **notificação de conclusão**, que acorda o Arquiteto (seção 3).
6. O Arquiteto lê o ID no título e no link, cruza com o livro-razão (seção 4) e, se houver casamento único, segue a fase e avisa o humano quando couber.

Se o ID não casar, vale a seção 5.

## 3. Notificação de conclusão: o que vem e o que não vem

Exemplo literal (teste `req-20261103-001`, trechos longos cortados com …):

```
Background task "Cloud agent bc-e3674a19-1e58-53b1-bbfa-eb88e2276620" (cursor-agent) finished:
The Cursor agent finished.
Agent: https://cursor.com/agents/bc-e3674a19-1e58-53b1-bbfa-eb88e2276620
No pull request link is available yet (the agent may have made no changes, or the PR is still being created).

Summary from the Cursor agent:
A branch `fix/20261103-versao-adega-v1-1` está no remoto, com o commit `44836f8`. Não abri pull request e não fiz merge.
…
<img src="/opt/cursor/artifacts/faixa-producao.png" alt="…" />
<img src="/opt/cursor/artifacts/faixa-vite-dev.png" alt="…" />
## Arquivos …
## Testes e build …
## Como ver …
```

**O que vem:**

| Campo | Onde aparece |
| --- | --- |
| Status | "finished" na primeira linha. Só foi visto o caso de conclusão; como chegam erro e timeout ainda não foi observado |
| ID do agente (`bc-…`) | no título da notificação e no link `Agent: https://cursor.com/agents/bc-…` |
| Resumo escrito pelo agente | branch, commit, arquivos alterados, testes e build, como ver a aplicação |
| Aviso de PR | linha informando que ainda não há link de pull request |
| Imagens | duas imagens (prints do agente); o caminho `/opt/cursor/artifacts/…` do texto só existe na VM do agente |

**O que NÃO vem:**

- slug e `request_id` (só existem no título que o Arquiteto dá ao agente e no livro-razão; não confiar no nome, porque o slug também usa traço);
- ID do modelo usado;
- duração da execução;
- link de PR (o agente não abre PR sem ordem; o aviso de "PR ainda não disponível" é padrão);
- campos estruturados: o resumo é texto livre escrito pelo agente. Por isso o prompt de lançamento deve pedir a branch e o commit em linhas fixas.

## 4. Como o Arquiteto casa o pedido

1. No lançamento, grava o **ID do agente** no livro-razão, junto do `request_id`.
2. Quando a notificação chega, extrai o ID (título ou link) e procura **exatamente** esse ID no livro-razão.
3. Se achar um único pedido, entrega a esse pedido e só a ele. Nunca casa por nome, slug, branch ou repositório.

## 5. Pedido órfão (notificação sem casamento)

Regra oficial, seção 9 da skill `arquiteto-operacao-cursor`:

- Se a notificação chegar e o ID do agente não casar com nenhum registro do livro-razão (ID não encontrado ou gravação que falhou no lançamento), o Arquiteto **avisa o humano** com os dados da notificação: branch, commit, arquivos e o link com o ID do agente.
- **Nunca entrega a ninguém sem casamento único.**
- O **humano identifica o pedido manualmente**, pela branch (padronizada com data por solicitação) ou indo ao repositório.
- O Arquiteto não tenta adivinhar o pedido por branch ou repositório e não relança nada.

## 6. Sem varredura de status

- Na V2 o Arquiteto lança o agente no Cursor e recebe de volta a notificação de conclusão. Não existe varredura de status.
- Se a notificação não chegar, o humano confere o agente pelo link `https://cursor.com/agents/bc-…`, com o ID gravado no livro-razão.

## 7. Limites conhecidos

- A notificação não traz o ID do modelo nem a duração: a plataforma escolhe o modelo, e a conferência real é pelo painel de uso.
- O dev server e o preview ficam na VM do agente, em endereços locais; sem túnel público o humano só vê os prints.
- Pendência de decisão do humano: modelo explícito no lançamento.

## 8. Fases, push, review e ambiente dev

O que acontece entre as fases (push ao final do implement, PR, review com a `the-judge`, merge, ambiente dev e produção) e a regra de sessão nova por fase estão nas skills `arquiteto-review-merge` e `arquiteto-fases` e nos documentos de `markdown/fases/`. Todo pedido ao Cursor, em qualquer fase, sai do Arquiteto e volta para ele pela notificação de conclusão.
