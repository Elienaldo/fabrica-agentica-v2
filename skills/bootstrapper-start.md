---
name: Bootstrapper — start
description: >-
  Carregue ao receber uma feature nova do humano: nome da feature, script de criação de seção, verificação da seção, encerramento e comunicação com o humano. Carregue também quando chegar um aviso de criação de seção. O encerramento da feature (handoff do Arquiteto) é a skill `bootstrapper-encerramento`.
---
# Bootstrapper — start

## 1. Receber a solicitação (passo a)
Registre o pedido original do humano como veio, sem reinterpretar. Se faltar o que é preciso para nomear a feature, pergunte ao humano (seção 6).

## 2. Nome da feature (passo b)
O nome da feature é o prefixo (`feat` ou `fix`), um hífen e o nome da feature em minúsculas com hífens, por exemplo `feat-nome-da-feature` (hífen no lugar da barra, que pode não ser aceita em título de seção).
- Use o nome exato desse pedido. Ninguém acrescenta prefixo nem converte maiúsculas automaticamente.
- Esse nome é o mesmo da seção da feature.
- Antes de seguir, confira se o nome já existe ativo (seção ou Arquiteto). Se existir, recuse e avise o humano.

## 3. Script de criação de seção (passo c)
Execute no PC-ELIENALDO (`01e97b36-f520-42d0-8a45-dc9c4d82d714`), por Shell com esse machineId:

```powershell
py -3 "C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\criar-secao-feature.py" "<nome-da-feature>"
```

O script cria só a seção da sidebar; não cria bots e não é sessão do Cursor. Sucesso exige exit 0 e relatório `CONCLUIDO`.

Regras do disparo: um disparo por pedido; registre pedido, nome e estado antes de disparar; sem retry automático após erro, timeout ou falha de aviso; uma notificação final nunca é novo start; estado incerto exige conferir o estado e avisar o humano, nunca relançar. Não use outro meio para criar a seção e não crie rotina, listener nem webhook por conta própria.

## 4. Verificar a seção (passo d)
- Confirme pela ferramenta sancionada do app que a seção da feature existe com o nome exato e sem ambiguidade (ListSections).
- Sem essa confirmação, ou com nome divergente, duplicado ou de outra feature, não siga para o passo (e): registre e avise o humano.

## 5. Encerrar (passo f)
Ao receber o ID do Arquiteto criado (`bootstrapper-criacao-arquiteto`), avise o humano em uma mensagem curta: nome da feature, seção confirmada, nome e ID do Arquiteto. Depois disso, o Bootstrapper não acompanha a feature: fica pronto para a próxima demanda.

## 6. Comunicação com o humano
- Linguagem comum, sem jargão, para pessoa não técnica.
- Fluxo dependendo de decisão humana ou parado: aviso no mesmo turno com estado atual em uma frase, o que entendeu da última resposta e as opções, sempre com resposta livre. Se já houver widget aguardando o humano, não abra outro.
- Ao apresentar consequência relevante, diga o que acontece se aprovar e se negar.
- Widget sempre com `allowCustom: true`; nunca um botão fictício "Outro".
- Esta regra não cria aprovação redundante nem amplia autorizações.

## 7. Avisos de criação da seção
- O Bootstrapper acorda também quando chega um aviso de criação de seção.
- O script `criar-secao-feature.py`, ao terminar (sucesso ou falha, desde que haja nome de seção válido), faz uma tentativa de POST para a rotina do Bootstrapper "Fábrica V2 — bloqueio criação" (variáveis `FABRICA_V2_CRIACAO_WEBHOOK_URL` e `FABRICA_V2_CRIACAO_WEBHOOK_KEY`).
- A rotina acorda o Bootstrapper, que só registra e avisa o humano no próprio chat: em sucesso, que a seção foi criada; em falha, o motivo da falha e a seção afetada. Não cria, não relança, não corrige e não aciona outro bot. HTTP 200 não prova que o humano leu.

## 8. Encerramento da feature
- Quando o Arquiteto avisa o encerramento (handoff com a autorização do humano) ou o humano pede o encerramento de uma feature, carregue `bootstrapper-encerramento`: o Bootstrapper valida o handoff pelas travas (`ListSections` e dry-run), roda `destruir-secao-api.py` (Arquiteto, depois a seção, depois os grupos) e reporta o resultado. Handoff do próprio Arquiteto que passa em todas as travas não pede nova confirmação do humano, porque ele já autorizou.
- A confirmação direta do humano continua obrigatória quando o pedido não vem do handoff do próprio Arquiteto da seção (remetente = `arquiteto_id`, dentro de `secao_id`) e em qualquer divergência. A autorização repassada por qualquer outro bot não vale como aprovação. O Bootstrapper nunca é alvo da exclusão e não exclui bots por conta própria, fora dessa skill.
