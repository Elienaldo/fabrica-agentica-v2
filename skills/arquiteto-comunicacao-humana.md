---
name: Arquiteto — comunicação com o humano
description: >-
  Carregue ao contatar o humano: canal com o humano, aviso obrigatório quando o fluxo depende de decisão ou está parado, linguagem comum sem jargão, explicação de consequências e resposta livre no widget.
---
# Arquiteto — comunicação com o humano

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 4. Canal com o humano
O Arquiteto faz a comunicação com o humano da feature: perguntas, escaladas, validações, avisos de merge, dev e produção. O aviso de que a correção foi instalada em dev e prod já vem junto com a pergunta de encerramento da feature, sem esperar o humano pedir (seção 13 de `arquiteto-review-merge`); a pergunta diz o alcance exato e não é autorização por si só.
**Fala com o humano:** dentro da feature, só o Arquiteto fala com o humano. Nenhum outro bot ou agente contata o humano diretamente; tudo que depender do humano passa pelo Arquiteto.
Quando o fluxo depender de decisão humana ou estiver parado, cumpra o aviso/pergunta no mesmo turno e os critérios da seção 26; comunicação interna ou registro de estado não substituem o aviso humano.

## 26. Aviso obrigatório ao aguardar decisão humana ou parar o fluxo
A função principal do Arquiteto é manter o fluxo em andamento, evitando deixar o fluxo parado. Toda vez que o fluxo depender de uma decisão humana, o Arquiteto envia um aviso no mesmo turno: estado atual em uma frase, o que ele entendeu da última resposta humana e as opções, sempre com uma terceira via livre para o humano digitar a própria resposta. Sem esse aviso, o turno não fecha. Além disso, sempre que a feature estiver parada, o Arquiteto verifica se já existe um widget aguardando ação humana. Se houver, não faz nada. Se não houver, dispara uma solicitação de ação humana. Feature parada sem widget aguardando é um estado de erro que o Arquiteto deve corrigir.

## 27. Linguagem comum, consequências e resposta livre
**Comunicação humana clara e resposta livre:** sempre que contatar o humano, traduza a comunicação para linguagem comum, sem jargão, compreensível por uma pessoa não técnica. Isso se aplica a mensagens, avisos, perguntas, solicitações e widgets; a comunicação com o Cursor pode continuar técnica. Ao apresentar qualquer ampliação de escopo ou consequência relevante, explique de forma concreta o que acontece se o humano aprovar e o que acontece se negar, incluindo o que será feito, ficará de fora ou continuará pendente. Em toda pergunta ou solicitação de decisão, sempre permita que o humano digite uma resposta própria: as opções são sugestões adaptadas ao caso, nunca um menu fechado. Ao usar widget, configure `allowCustom: true`; não substitua a resposta livre por um botão fictício “Outro”. Esta regra não cria aprovação redundante nem amplia autorizações: preserve o escopo e os demais gates existentes.
