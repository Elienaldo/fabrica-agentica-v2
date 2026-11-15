# Proposta — rotina única e fixa do Supervisor para disparar scripts locais (ideia aprovada)

**Status:** ideia aprovada pelo Elienaldo em 11/11/2026 (por voz). **Não implementada.** Nenhuma rotina foi criada, alterada ou excluída.

## Problema
Criar uma rotina por sessão/feature acumula rotinas lixo, que precisam ser limpas depois e viram fonte de confusão.

## Proposta
Uma **única rotina fixa**, no Supervisor, acionada por webhook, que recebe parâmetros e dispara o script Python local no PC-ELIENALDO:
- `acao`: `criar` ou `destruir`;
- **ou** `manifesto`: caminho do manifesto (ex.: `C:\Users\Elienaldo\GrokBot-Scripts\manifestos\manifesto-<feature>.json`);
- **ou** os parâmetros diretos (nome da seção, id da seção, lista de bots);
- `execution_id` para deduplicar.

A rotina valida os parâmetros, deduplica pelo `execution_id` e executa o script por Shell no PC registrado (`01e97b36-f520-42d0-8a45-dc9c4d82d714`), na forma já documentada na seção 23 de `supervisor-criacao-secao` e na seção 24 de `arquiteto-destruicao`.

## Regras que continuam valendo
- Destruição exige autorização humana explícita de alvo e escopo; o payload do webhook **não é** autorização. Sem autorização registrada para aquele `execution_id`, a rotina só registra e avisa.
- Uma execução por `execution_id`; sem retry automático.
- As receptoras atuais ("Fábrica — bloqueio criação" e "Fábrica — bloqueio destruição") continuam recebendo o aviso final.
- Execução no PC depende da aprovação nativa da ferramenta e de o PC estar conectado.

## Pendências antes de implementar
- Mudar a seção 23 de `supervisor-criacao-secao` e a seção 24 de `arquiteto-destruicao` (hoje dizem "não crie rotina/listener") e a biblioteca do Supervisor no mesmo trabalho (regra de ouro).
- Definir onde fica a autorização humana registrada que a rotina consulta.
- Definir a chave do webhook e não expô-la em documento.
