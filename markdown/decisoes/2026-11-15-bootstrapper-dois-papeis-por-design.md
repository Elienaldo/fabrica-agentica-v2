# Decisão: o Bootstrapper tem dois papéis por design

**Data:** 15/11/2026, por volta das 22h30 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi decidido
O Bootstrapper acumula dois papéis de propósito, e isso não é pendência nem problema:
1. dar a partida da feature: nome, script de criação de seção e criação do Arquiteto;
2. receber os avisos de bloqueio dos webhooks dos scripts e repassar ao humano.

## Por quê
O aviso de bloqueio do script de destruição pode chegar quando o Arquiteto da feature já não existe. Por isso, a devolução ao humano fica com o Bootstrapper, que é permanente.

## O que mudou
- `README.md`: entrou uma linha logo abaixo da tabela de bots (seção 1) dizendo que os dois papéis são por design, com o motivo. O README não tratava isso como pendência. Hash `695E012E` → `D5AD39F3`.
- Backup: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\bootstrapper-dois-papeis-20261115-2230`.
- Releitura: a comparação com o backup mostra só a linha nova e uma linha em branco.

## Menções encontradas e não alteradas
- `checklist-v2.html:80`: nota histórica de 14/11/2026 no Kanban ("o Supervisor se transformou no Bootstrapper, que assume dois papéis"). É registro de um momento.
- `markdown/modelos/bootstrapper.md:5`: diz "Job único: dar a partida... Faz SÓ isto", mas a mesma ficha também traz o "Aviso de bloqueio da destruição". O texto não trata isso como problema, mas o "Faz SÓ isto" pode ser lido como contradição. Não alterei, porque não fazia parte do pedido.
- Nenhuma skill do box nem de `V2/skills` fala em "dois jobs" como problema.

## Commit
Não houve commit.
