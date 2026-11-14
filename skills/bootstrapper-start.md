---
name: Bootstrapper — start
description: >-
  Carregue ao receber uma feature nova do humano: nome da feature, script de criação de seção, criação do grupo inicial, verificação de seção e grupo, encerramento e comunicação com o humano.
---
# Bootstrapper — start

## 1. Receber a solicitação (passo a)
Registre o pedido original do humano como veio, sem reinterpretar. Se faltar o que é preciso para nomear a feature, pergunte ao humano (seção 7).

## 2. Nome da feature (passo b)
O nome da feature é o prefixo (`feat` ou `fix`), um hífen e o nome da feature em minúsculas com hífens, por exemplo `feat-nome-da-feature` (hífen no lugar da barra, que pode não ser aceita em título de seção).
- Use o nome exato desse pedido. Ninguém acrescenta prefixo nem converte maiúsculas automaticamente.
- Esse nome é o mesmo da seção da feature e entra nos nomes dos grupos: `canal-<nome-da-feature>` (grupo inicial) e `<fase>-<nome-da-feature>` (grupos de fase).
- Antes de seguir, confira se o nome já existe ativo (seção, grupo ou Arquiteto). Se existir, recuse e avise o humano.

## 3. Script de criação de seção (passo c)
Execute no PC-ELIENALDO (`01e97b36-f520-42d0-8a45-dc9c4d82d714`), por Shell com esse machineId:

```powershell
py -3 "C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\criar-secao-feature.py" "<nome-da-feature>"
```

O script cria só a seção da sidebar; não cria grupo nem bots e não é sessão do Cursor. Sucesso exige exit 0 e relatório `CONCLUIDO`.

Regras do disparo: um disparo por pedido; registre pedido, nome e estado antes de disparar; sem retry automático após erro, timeout ou falha de aviso; uma notificação final nunca é novo start; estado incerto exige conferir o estado e avisar o humano, nunca relançar. Não use outro meio para criar a seção e não crie rotina, listener nem webhook por conta própria.

## 4. Criar o grupo inicial (após o passo c)
Com a seção confirmada, crie pelo app o grupo inicial da feature, com o nome exato `canal-<nome-da-feature>`. É um grupo só por feature, em qualquer caminho. Não crie grupo de fase aqui. Registre no log o nome do grupo e o ID devolvido pelo app. Se a criação falhar, não repita em laço: registre e avise o humano.

## 5. Verificar seção e grupo (passo d)
- Confirme pela ferramenta sancionada do app que a seção da feature existe com o nome exato e sem ambiguidade (ListSections).
- Confirme que o grupo `canal-<nome-da-feature>` criado no passo 4 existe, com o nome exato e o mesmo ID registrado no log.
- Sem as duas confirmações, ou com nome divergente, duplicado ou de outra feature, não siga para o passo (e): registre e avise o humano.

## 6. Encerrar (passo f)
Ao receber o ID do Arquiteto criado (`bootstrapper-criacao-arquiteto`), avise o humano em uma mensagem curta: nome da feature, seção e grupo confirmados, nome e ID do Arquiteto. Depois disso, o Bootstrapper não acompanha a feature: fica pronto para a próxima demanda.

## 7. Comunicação com o humano
- Linguagem comum, sem jargão, para pessoa não técnica.
- Fluxo dependendo de decisão humana ou parado: aviso no mesmo turno com estado atual em uma frase, o que entendeu da última resposta e as opções, sempre com resposta livre. Se já houver widget aguardando o humano, não abra outro.
- Ao apresentar consequência relevante, diga o que acontece se aprovar e se negar.
- Widget sempre com `allowCustom: true`; nunca um botão fictício "Outro".
- Esta regra não cria aprovação redundante nem amplia autorizações.
