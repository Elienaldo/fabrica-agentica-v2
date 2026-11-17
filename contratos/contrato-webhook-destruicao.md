# Contrato — execução da destruição pelo Bootstrapper e aviso ao humano (V2)

## Quem dispara
- O **Bootstrapper** roda o script no PC, só depois do handoff de encerramento do próprio Arquiteto da seção, que já traz a autorização do humano, e das travas (dry-run incluso); fora do handoff, só com a confirmação direta do humano (alvo e alcance), conforme `contratos\contrato-destruicao-api-interna.md` e a skill `bootstrapper-encerramento`:

```powershell
py -3 "C:\Users\Elienaldo\Projetos\Fabrica-Agentica-V2\scripts\destruir-secao-api.py" --secao-id "<id da seção>" --api-real
```

- Sem `--executar` é só planejamento (dry-run), usado pelo Bootstrapper para validar o handoff. Execução real e regras de confirmação: ver o contrato de API interna.
- O **Arquiteto não roda o script e não exclui nada**: só avisa o Bootstrapper (handoff de encerramento).
- Fim da feature, merge ou aprovação, sozinhos, não autorizam destruir. A autorização repassada por outro bot (que não seja o handoff do Arquiteto da seção) não vale como aprovação.

## Bot protegido
- **Somente o Bootstrapper** (por ID ou nome exato). Se aparecer no alvo, o script para antes de excluir qualquer coisa.

## Saída
- JSON no terminal e linha no log `scripts\logs\destruir-secao-api.jsonl`, com `status`, `erro`, `stage`, `needs_human_notification` e `motivos_aviso_humano`.
- Exit: 0 sucesso ou dry-run; 2 bloqueio; 1 falha.

## Aviso ao humano (sem webhook)
- Desde 17/11/2026 o script **não envia aviso por webhook**. O chamador é o próprio Bootstrapper, que leu o resultado e avisa o humano, em linguagem comum, de sucesso, falha ou bloqueio: feature, o que foi excluído e o que ficou.
- Todo bloqueio ou falha sai com `needs_human_notification=true` e o motivo em `erro` e `motivos_aviso_humano`.
- Exit 2, falha ou estado incerto não são sucesso. O aviso nunca autoriza nova tentativa de exclusão: rodar de novo é outra execução, só com nova confirmação do humano.

## Legado (sem uso)
- `scripts\notificacao_bootstrapper.py`, as variáveis `FABRICA_V2_WEBHOOK_URL` e `FABRICA_V2_WEBHOOK_KEY` e a rotina do Bootstrapper "Fábrica V2 — bloqueio destruição" ficam sem chamador. A rotina existe no app e pode ser desativada pelo humano. O aviso de criação de seção (`contrato-webhook-criacao.md`) não mudou.
