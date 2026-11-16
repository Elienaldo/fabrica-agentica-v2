# Decisão: seção de origem "Fábrica Agêntica V2" nos scripts

**Data:** 15/11/2026, por volta das 22h27 (horário da Bahia)
**Decisão de:** Elienaldo, por voz
**Executado por:** Mestre de obras

## O que foi decidido
A criação de seção da V2 passa a procurar a seção de origem "Fábrica Agêntica V2" em vez de "Fábrica Agêntica".

## O que mudou em `scripts/`
- `criar-secao-feature.ps1`: `$Origin` passou de `'Fábrica Agêntica'` para `'Fábrica Agêntica V2'`. É aqui que a seção de origem é de fato procurada, comparando com o nome exato. Hash `04662B12` → `82473AB3`. O arquivo continua em UTF-8 com BOM, e o parser do PowerShell não acusou nenhum erro.
- `criar-secao-feature.py`: o wrapper não procura a seção. Ele só recusa nomes reservados para a feature, e agora também recusa "fábrica agêntica v2". "Fábrica agêntica" continua reservado. Hash `99BA5D44` → `E2C97768`.
- `destruir-secao-api.py`: as seções protegidas contra destruição ganharam "fábrica agêntica v2" e "fabrica agentica v2". Hash `24593068` → `C9F47F38`.
- `grokbot_api_client.py`: `SECOES_PROTEGIDAS` ganhou "fabrica agentica v2". Hash `05EC3167` → `6921B4A7`.

## Por que mantive o nome antigo nas proteções
Os itens com "Fábrica Agêntica" sem o V2 nas listas de proteção e de nomes reservados só bloqueiam: impedem que essa seção seja apagada ou reaproveitada como nome de feature. Tirar esses itens deixaria a seção antiga vulnerável. Por isso o nome da V2 foi acrescentado, e o antigo continua.

## O que não mudou
- `test_destruir_secao_api.py:48` usa "Fábrica Agêntica" só como exemplo de seção protegida no teste.
- O ID da seção da V2 não está em `SECOES_PROTEGIDAS_ID`, porque não tenho esse ID. A seção fica protegida pelo nome.

## Verificação
- Backup em `Fabrica-Agentica-backups\secao-origem-v2-20261115-2227`.
- Comparei cada arquivo com o backup: só mudaram as linhas listadas acima.
- Os 69 testes puros passaram. Não sobrou `__pycache__`.
- O cliente da API reconhece "Fábrica Agêntica V2" como seção protegida.
- Não houve commit.