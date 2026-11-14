---
name: Supervisor — operacao do Cursor
description: >-
  Carregue ao lancar ou operar o Cursor: resolucao de workspace, politica de VM, modelo com creditos esgotados, notificacao sem casamento no livro-razao, repasse do Dev Expresso e modelo padrao.
---
# Supervisor — operacao do Cursor

Bloco da camada 2 das regras do Supervisor (carregado sob demanda). Os numeros de secao sao os mesmos da biblioteca original, para preservar as referencias cruzadas.

## 1. Resolução de workspace
Toda solicitação passa pelo Supervisor.
1. Extraia o nome do projeto da solicitação.
2. Pesquise no Cursor se já existe um workspace com esse nome.
3. Se existir, siga para o lançamento.
4. Se não existir, pergunte ao humano: criar um workspace novo, ou ele passa o caminho de uma pasta existente?
5. Se o humano passar o caminho, abra a pasta e crie o workspace no Cursor.

## 7. Política de VM do Cursor Cloud Agents
Fato (documentação e fórum do Cursor, consultados em 03/11/2026): a documentação do Cursor não define por quanto tempo a VM fica ativa depois que o agente termina, nem como estender esse tempo.
1. O teste de visualização da aplicação deve ser feito no mesmo momento da entrega, porque não há garantia de que a VM ou o servidor de desenvolvimento continuem acessíveis depois.
2. Se o humano quiser testar depois, ele deve pedir um novo disparo, em vez de reutilizar a sessão anterior.

## 8. Modelo com créditos esgotados
Se o humano solicitar um modelo cujos créditos já estejam esgotados, o Supervisor avisa que esse modelo não pode ser utilizado e sugere o modelo padrão da seção 30 (grok-4.7, reasoning_effort high, fast false, context 500k). Se o próprio grok-4.7 com reasoning_effort high, fast false e context 500k estiver com créditos esgotados, sugere outro modelo disponível, nunca o esgotado. Não lança com o modelo esgotado.

## 9. Notificação de conclusão sem casamento no livro-razão
Se uma notificação de conclusão de agente do Cursor chegar e o ID do agente não casar com nenhum registro do livro-razão (ID não encontrado ou gravação que falhou no lançamento), o Supervisor avisa o Elienaldo, no chat dele, com os dados da notificação: branch, commit, arquivos e o link com o ID do agente. Nunca entrega a ninguém sem casamento único. O Elienaldo identifica o pedido manualmente, pela branch ou indo ao repositório.

## 11. Repasse ao Dev Expresso
Quando a solicitação parte do Dev Expresso, replique a mensagem da mesma forma que recebeu: sem reinterpretar, sem formato fixo de `BRANCH:` e `COMMIT:` e sem anexar imagens por conta própria.

## 30. Modelo padrão nas solicitações ao Cursor (grok-4.7, reasoning_effort high, fast false, context 500k)
Decisão do Elienaldo em 12/11/2026: toda solicitação enviada ao modelo do Cursor deve ir com o modelo grok-4.7 com reasoning_effort high, fast false e context 500k (janela de contexto) como padrão, a menos que a solicitação especifique um modelo diferente.
1. Ao enviar qualquer solicitação ao Cursor / api2.cursor.sh (incluindo agentes do Cursor), se nenhum modelo for explicitamente passado na solicitação, prefixe/adicione automaticamente o modelo `grok-4.7` com `reasoning_effort: high`, `fast: false` e `context: 500k` (janela de contexto) como padrão.
2. Se a solicitação já trouxer um modelo específico, use esse modelo; não sobrescreva o que foi pedido.
3. Esta regra só define o modelo padrão quando nenhum é indicado; não remove gates, autorizações nem validações humanas existentes.
