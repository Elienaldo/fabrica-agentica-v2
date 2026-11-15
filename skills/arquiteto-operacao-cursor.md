---
name: Arquiteto — operação do Cursor
description: >-
  Carregue ao lançar ou operar o Cursor: resolução de workspace, regra de branch, lançamento e livro-razão, visualização de UI, política de VM, modelo com créditos esgotados, notificação sem casamento no livro-razão e modelo padrão.
---
# Arquiteto — operação do Cursor

Bloco da camada 2 das regras do Arquiteto (carregado sob demanda). Os números de seção resolvem pelo índice de `arquiteto-regras`.

## 1. Resolução de workspace
Toda solicitação passa pelo Arquiteto.
1. Extraia o nome do projeto da solicitação.
2. Pesquise no Cursor se já existe um workspace com esse nome.
3. Se existir, siga para o lançamento.
4. Se não existir, pergunte ao humano: criar um workspace novo, ou ele passa o caminho de uma pasta existente?
5. Se o humano passar o caminho, abra a pasta e crie o workspace no Cursor.

## Lançamento e livro-razão
O Arquiteto é a ponte entre a feature e o Cursor. Para cada fase liberada, lança o agente de nuvem pela API v1 do Cursor, usando a ferramenta de agente de nuvem do Cursor (que já tem a chave), com `name` como `slug|fase|request_id`. Mantém o livro-razão (`request_id → agent_id → grupo/feature/fase`) e o índice de branches (feature → branch). O retorno chega pela notificação de conclusão do agente de nuvem (não há webhook). Casa o ID do agente da notificação com o livro-razão: casando, segue a fase; sem casar, é pedido órfão (seção 9). Se a notificação indicar erro, avisa o humano.

**Proteção contra lançamento repetido:**
1. Antes de lançar um agente, registre o estado no livro-razão (`request_id`, fase e grupo/feature); só lance depois do registro gravado.
2. Se o estado do lançamento for incerto (gravação que falhou, retorno sem ID do agente ou dúvida se o agente já foi criado), não relance: reconcilie consultando o Cursor e o livro-razão e, se não resolver, avise o humano.
3. Notificação duplicada nunca relança: a mesma notificação de conclusão recebida mais de uma vez é tratada uma única vez.

## Regra de branch
Todo pedido novo ganha branch nova (`feat/` ou `fix/YYYYMMDD-nome-da-task`), sem exceção, qualquer que seja o tamanho; nunca a `main`. Pedido que cita algo do índice com branch aberta é continuação e usa a mesma. Se nada casa, é novo: verificar ou criar a branch não abre sessão própria; a criação da branch vai combinada com a solicitação completa da fase numa única comunicação ao modelo do Cursor (seção 21 de `arquiteto-fases`).

## Visualização de UI
Quando o agente do Cursor subir um servidor dev, o Arquiteto exige, no prompt de lançamento e no relatório final, uma URL pública acessível (via túnel, como Cloudflare Tunnel ou ngrok) para o humano ver a aplicação no navegador, em vez de só endereços localhost. Sem a URL pública, o Arquiteto avisa o humano de que só há prints.

## 7. Política de VM do Cursor Cloud Agents
A documentação do Cursor não define por quanto tempo a VM fica ativa depois que o agente termina, nem como estender esse tempo.
1. O teste de visualização da aplicação deve ser feito no mesmo momento da entrega, porque não há garantia de que a VM ou o servidor de desenvolvimento continuem acessíveis depois.
2. Se o humano quiser testar depois, ele deve pedir um novo disparo, em vez de reutilizar a sessão anterior.

## 8. Modelo com créditos esgotados
Se o humano solicitar um modelo cujos créditos já estejam esgotados, o Arquiteto avisa que esse modelo não pode ser utilizado e sugere o modelo padrão da seção 30 (grok-4.7, reasoning_effort high, fast false, context 500k). Se o próprio grok-4.7 com reasoning_effort high, fast false e context 500k estiver com créditos esgotados, sugere outro modelo disponível, nunca o esgotado. Não lança com o modelo esgotado.

## 9. Notificação de conclusão sem casamento no livro-razão
Se uma notificação de conclusão de agente do Cursor chegar e o ID do agente não casar com nenhum registro do livro-razão (ID não encontrado ou gravação que falhou no lançamento), o Arquiteto avisa o humano com os dados da notificação: branch, commit, arquivos e o link com o ID do agente. Nunca entrega a ninguém sem casamento único. O humano identifica o pedido manualmente, pela branch ou indo ao repositório.

## 30. Modelo padrão nas solicitações ao Cursor (grok-4.7, reasoning_effort high, fast false, context 500k)
Toda solicitação enviada ao modelo do Cursor vai com o modelo grok-4.7 com reasoning_effort high, fast false e context 500k (janela de contexto) como padrão, a menos que a solicitação especifique um modelo diferente.
1. Ao enviar qualquer solicitação ao Cursor / api2.cursor.sh (incluindo agentes do Cursor), se nenhum modelo for explicitamente passado na solicitação, prefixe/adicione automaticamente o modelo `grok-4.7` com `reasoning_effort: high`, `fast: false` e `context: 500k` (janela de contexto) como padrão.
2. Se a solicitação já trouxer um modelo específico, use esse modelo; não sobrescreva o que foi pedido. Se o humano solicitar um modelo específico no início do fluxo, ele segue em todas as fases até o final; a troca de modelo no meio do fluxo não é automática.
3. Esta regra só define o modelo padrão quando nenhum é indicado; não remove gates, autorizações nem validações humanas existentes.
