# Decisão: documentos da fábrica anterior adaptados para a V2

**Data:** 15/11/2026, entre 22h24 e 22h30 (horário da Bahia)
**Decisão de:** Elienaldo, por voz
**Executado por:** Mestre de obras

## O que foi decidido
1. **Adaptar** `markdown/modelos/fábrica-agêntica.md` para `markdown/modelos/fábrica-agêntica-v2.md`. O documento geral foi mantido, com Bootstrapper na entrada, Arquiteto como único bot da feature e Âncora V2 como alvo do script de criação. Foram mantidos o catálogo de skills, os limites de rodadas e as regras transversais. Saíram Supervisor, Dr. Eggbot, Principal, Orquestrador, Cirurgião e Curador, e o fluxo, o mermaid, a tabela "Quem é quem" e os caminhos foram refeitos. As fontes foram o README, as fichas, as skills `arquiteto-*` e `bootstrapper-*` e os documentos de fase. O arquivo antigo foi apagado da V2 e está no backup.
2. **Descartar** `markdown/prompt-research-enxuto.md`, um prompt de uso único de uma feature antiga, com caminho da V1. Foi apagado da V2 depois do backup e do hash, e não sobrou cópia na V2.
3. **Adaptar** três documentos:
   - `markdown/comunicacao.md`: um grupo por fase, `<fase>-<feature>`, criado pelo Arquiteto, só com ele e o humano, e o Cursor fora dos grupos. As seções 5 e 6 ficaram com a mesma numeração, e da seção 7 ficaram os pontos sobre o prefixo e o dono do ADR.
   - `markdown/regras/convencoes-fabrica.md`: saíram o roteamento do Supervisor, "Dev Expresso avaliado", a lista da regra 28 por bot (com a linha ambígua do Âncora) e o trecho `canal-`/Supervisor. "Criação de bots" passou ao Bootstrapper, a partir de `markdown/modelos/arquiteto.md`. Os caminhos da V1 foram corrigidos e saiu o "inclusive Dr. Eggbot".
   - `markdown/automacoes/comunicacao-bidirecional-cursor.md`: o Arquiteto entrou no lugar do Supervisor. Ficaram as seções 3, 4, 5 e 7. Saíram o caminho do Dev Expresso e a cadeia Principal → Supervisor → Orquestrador; as antigas seções 8 a 11 viraram um ponteiro para as skills `arquiteto-review-merge` e `arquiteto-fases`. A seção 6 (varredura) virou pendência.

## Ajustes pedidos durante a mesma tarefa
- **Arquiteto criado dinamicamente:** o Arquiteto não é criado à mão no app. O Bootstrapper roda o script que cria a seção da feature e então cria o Arquiteto exclusivo daquela feature. No README, a pendência "Criar o bot Arquiteto no app" saiu, e a regra entrou no aviso de estado, na tabela de bots e na seção 4. A regra também está em `fábrica-agêntica-v2.md` e em `convencoes-fabrica.md`.
  - A varredura achou textos a corrigir só no README. Os diagramas `.excalidraw`, as fichas, os contratos, `V2/skills` e as skills `bootstrapper-*` e `arquiteto-*` do box já descrevem a criação pelo Bootstrapper. Nenhum diagrama e nenhuma skill foram alterados.
  - Registro histórico não alterado: `markdown/decisoes/2026-11-15-arquiteto-destruicao-sem-resultado-json.md:20` ("o bot Arquiteto ainda não foi criado").
- **Seção de origem Fábrica Agêntica V2:** decisão `2026-11-15-secao-origem-fabrica-agentica-v2.md`; os scripts não foram tocados aqui. A devolução do Âncora V2 passou a citar "Fábrica Agêntica V2" no README (tabela de bots e seção 4), em `contratos/contrato-webhook-criacao.md` e em `fábrica-agêntica-v2.md`. No README, as seções protegidas passaram a incluir "Fábrica Agêntica V2".
- **Pendências do README:** saíram as rotinas e variáveis (já configuradas, ver `2026-11-15-variaveis-webhook-criacao-v2.md`), trocadas por "testar de verdade os avisos por webhook". Também saíram a proposta de rotina única (já excluída, ver `2026-11-15-remocao-proposta-rotina-unica-supervisor.md`), a lista dos 5 documentos (tratados aqui) e "Criar o bot Arquiteto no app". O aviso de estado no topo do README e a seção 6 também foram atualizados sobre rotinas e variáveis. Entrou a pendência da varredura.

## Arquivos e hashes (SHA-256, 8 primeiros caracteres)
| Arquivo | Ação | Antes | Depois |
|---|---|---|---|
| `markdown/modelos/fábrica-agêntica.md` | apagado (substituído pelo v2) | `C6DDDBE3` | — |
| `markdown/modelos/fábrica-agêntica-v2.md` | criado | — | `0547C109` |
| `markdown/prompt-research-enxuto.md` | apagado | `21D8CDA3` | — |
| `markdown/comunicacao.md` | alterado | `E594B2C0` | `BC86CAB1` |
| `markdown/regras/convencoes-fabrica.md` | alterado | `5F90013C` | `423EFCE0` |
| `markdown/automacoes/comunicacao-bidirecional-cursor.md` | alterado | `E52567A8` | `69BA2615` |
| `README.md` | alterado | `4020F84C` | `695E012E` |
| `contratos/contrato-webhook-criacao.md` | alterado | `B9A4BC0B` | `55B9A0FD` |

O README mudou de novo logo depois, por causa de `2026-11-15-bootstrapper-dois-papeis-por-design.md` (`695E012E` → `D5AD39F3`).

## Conferência
- Releitura de cada arquivo salvo: os hashes no PC batem com os gerados.
- A codificação foi mantida: tudo continua sem BOM. `convencoes-fabrica.md` e `fábrica-agêntica-v2.md` usam CRLF, como o original, e os outros usam LF. Não há caractere de substituição nem mojibake.
- Os caminhos citados nos arquivos alterados existem. O nome `fábrica-agêntica.md`, citado em `fábrica-agêntica-v2.md`, aponta para a cópia no backup, de propósito.
- Não sobrou referência a `prompt-research-enxuto.md` nem a `fábrica-agêntica.md` na V2, fora o ponteiro para o backup.
- Nenhuma skill mudou. As referências à "seção 5" de `comunicacao.md` nas fases e nas skills continuam válidas.
- A referência em `excalidraw/acompanhamento/teste-webhook-cursor-grokbot.excalidraw` continua válida e não foi tocada.

## Backup
`C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\docs-v1-para-v2-20261115-2225`: os 6 documentos originais, mais `contratos/contrato-webhook-criacao.md`.

## Pendências
- **Varredura de status dos agentes do Cursor:** não há evidência de que a rotina exista na V2. Nenhum documento da V2, nenhuma skill `arquiteto-*` e nem a ficha do Arquiteto citam a rotina. A seção 6 do documento de comunicação com o Cursor e o README registram como decisão pendente.
- **Descrição do Bootstrapper no app:** não consigo editar. A ficha e as skills `bootstrapper-*` não citam nenhum dos documentos alterados, então não há ajuste obrigatório. Opcional: a skill `bootstrapper-criacao-arquiteto` não diz que o Arquiteto é criado a partir da ficha `markdown/modelos/arquiteto.md`, como agora diz `convencoes-fabrica.md`.
- **Bot protegido:** o README (seção 5) diz "Único bot protegido: o Bootstrapper", mas o cliente da API também protege outros IDs. Não alterei; fica para conferir.

## Commit
Não houve commit.
