---
name: Bootstrapper — criação do Arquiteto
description: >-
  Carregue ao criar o bot Arquiteto da feature, depois de confirmar a seção: papel, local de criação, recusa de duplicata e entrega.
---
# Bootstrapper — criação do Arquiteto

## 1. Pré-condição
Só crie o Arquiteto depois do passo (d) de `bootstrapper-start`: seção da feature confirmada com o nome exato. Sem isso, não crie.

## 2. Criar o Arquiteto
Crie o bot Arquiteto dentro da seção da feature, resolvida pelo nome exato. O Arquiteto é o único bot responsável pela feature de ponta a ponta: branch, fases, Cursor, review, merge e instrução. Tudo isso é dele, não do Bootstrapper.

## 3. Local de criação
- Obtenha a lista real de seções (ListSections), resolva o nome da feature sem ambiguidade e só então crie o bot (CreateAgent) dentro dessa seção.
- Não use ID tirado de tela, RuntimeId ou AutomationId, nem aceite payload como confirmação.
- Se não conseguir resolver a seção, não crie em outro lugar: avise o humano.

## 4. Recusa de ID ativo ou duplicado
Se já existir um Arquiteto ativo para esse nome de feature, recuse e avise o humano. Nunca reaproveite o bot de outra feature e não crie duplicata.

## 5. Entrega
Depois de criar, confirme que o bot existe dentro da seção certa e devolva ao passo (f) de `bootstrapper-start`: nome da feature, nome e ID do Arquiteto, seção. O handoff ao Arquiteto leva só o pedido original do humano e o nome da feature (regra 28), sem o fio da conversa.

## 6. Limites
- Só exclui (o Arquiteto, a seção e os grupos da feature) no encerramento da feature, depois do handoff do próprio Arquiteto, que já traz a autorização do humano, ou com confirmação humana direta quando o pedido não vem desse handoff (`bootstrapper-encerramento`); nunca outro bot nem a si mesmo.
- Não cria rotina, listener ou webhook.
