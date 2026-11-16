# Decisão: ficha do Bootstrapper com dois papéis por design

**Data:** 15/11/2026, por volta das 22h34 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi decidido
A ficha do Bootstrapper deixa de dizer "Job único… Faz SÓ isto" e passa a registrar os dois papéis intencionais, conforme `2026-11-15-bootstrapper-dois-papeis-por-design.md`.

## O que mudou
Em `markdown/modelos/bootstrapper.md`, a linha "**Job único:** dar a partida de cada feature da Fábrica Agêntica V2 e sair de cena. Faz SÓ isto, nesta ordem:" foi trocada por:

> **Dois papéis, por design:** (1) dar a partida de cada feature da Fábrica Agêntica V2 (criar a seção pelo script e o Arquiteto da feature) e sair de cena; (2) repassar ao humano os avisos de bloqueio dos webhooks de criação e destruição. O segundo papel fica com o Bootstrapper porque o aviso de bloqueio da destruição pode chegar quando o Arquiteto da feature já não existe.
>
> **Papel 1, partida da feature**, nesta ordem:

Os passos de (a) a (f) e o resto da ficha não mudaram.

- Hash SHA-256: `840AE5F5` → `4A34BB81`.
- A codificação foi mantida: sem BOM, com LF.
- Backup: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\ficha-bootstrapper-dois-papeis-20261115-2234`.
- Releitura: a comparação com o backup mostra só esse trecho.

## Descrição do bot no app
A descrição atual do Bootstrapper (`f99cfa31…`) era idêntica à ficha inteira antes desta mudança, tirando a quebra de linha final. Agora está desatualizada só nesse trecho. Para alinhar, a descrição deve receber a ficha nova inteira. Não editei a descrição.

## Commit
Não houve commit.


## Atualização 22:38 Bahia: descrição no app
- Descrição do bot Bootstrapper (f99cfa31) no app substituída pela ficha nova inteira (regra de ouro). Antes 1C5FCD0E (3624 chars) → depois 03003966 (3937 chars), idêntica à ficha 4A34BB81 (ignorando CRLF e quebra final). Backup: /workspace/backups/bootstrapper-descricao-app-20261115-2237 (box).
