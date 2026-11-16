# Decisão: remover da V2 as citações de evidência de teste da V1

**Data:** 15/11/2026, por volta das 22h33 (horário da Bahia)
**Decisão de:** Elienaldo
**Executado por:** Mestre de obras

## O que foi decidido
Evidência de teste da V1 não fica na V2: se o teste não foi executado na V2, a referência não faz sentido. Saíram só as citações de evidência. As regras da etapa 6 continuam valendo.

## O que mudou
| Arquivo | Mudança | SHA-256 antes | SHA-256 depois |
|---|---|---|---|
| `contratos/contrato-destruicao-api-interna.md` | saiu a seção "## Evidência da etapa 6", que só tinha o caminho `GrokBot-Scripts\diagnostico-apiinterna-stage6-1113\`, junto com a linha em branco antes dela; o arquivo termina em "## Segurança" | `7982A211` | `7966601C` |
| `skills/arquiteto-destruicao.md` (PC) | item 8: saiu só o parêntese "(evidência em …RESUMO-stage6.md)"; "Exige a capacidade `api_interna.room_delete`, validated=true." continua | `0591B2F9` | `1E94BB31` |
| `/home/box/agent-data/workflows/arquiteto-destruicao/SKILL.md` (box) | a mesma mudança | `0591B2F9` | `1E94BB31` |

- O box e o PC continuam idênticos, com o mesmo hash.
- A codificação foi mantida: sem BOM, com LF e com quebra de linha no fim.
- Releitura: a comparação com o backup mostra só as remoções.

## Backup
- PC: `C:\Users\Elienaldo\Projetos\Fabrica-Agentica-backups\evidencia-v1-remocao-20261115-2233`
- Box: `/workspace/backups/evidencia-v1-remocao-20261115-2233`

## Descrição de bot no app
O Arquiteto é criado dinamicamente, então não há descrição fixa para alinhar. A ficha `markdown/modelos/arquiteto.md`, a ficha e a descrição do Bootstrapper e as skills `bootstrapper-*` não citam essa evidência.

## Pendência (não alterado)
- `scripts/destruir-secao-config.json:68`: o campo `validation_evidence` de `room_delete` cita `diagnostico-apiinterna-stage6-1113/...`. Na linha 63, o de `section_delete` cita `diagnostico-apiinterna-stageB-1112/...`.
- Não alterei porque `destruir-secao-api.py` (linha 117) só trata a capacidade como validada se `validation_evidence` estiver preenchido. Esvaziar o campo bloquearia a exclusão de grupos e de seção. Mudar isso exige decisão do humano, por exemplo trocar pelo texto de uma evidência da V2.

## Commit
Não houve commit.
