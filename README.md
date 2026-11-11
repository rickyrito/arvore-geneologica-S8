# Genealogia do Soito (Sabugal)

Página: https://rickyrito.github.io/arvore-geneologica-S8/

Dados transcritos dos assentos paroquiais do Soito publicados no blogue [Saber Soito](https://soitoribacoa.blogspot.com/) (294 artigos, 1624-1984).

## Página
- `index.html` + `dados.js` + `dados_s8.js` — explorador: 22 207 pessoas da base e 9 do suplemento S8, com filtros por família e origem. Página não indexada.
- O suplemento inicial lê os campos essenciais de três batismos do B1 (1692–1705): Isabel e Manuel em 26/12/1692, e Manuel em 30/12/1692. Cria três núcleos; não estabelece identidades com pessoas das genealogias existentes.
- Nas primeiras cinco imagens, a capa e a introdução não deram assentos individuais; 16 outros assentos ficam pendentes. A leitura é parcial, com excertos e dúvidas guardados, e não uma transcrição diplomática integral.

## GEDCOM
- `familia_soito.ged` — base anterior da freguesia: 22 207 indivíduos, 9253 núcleos familiares
- `assentos_s8.ged` — suplemento de originais S8: 9 indivíduos, 3 núcleos; não está incluído no GEDCOM anterior
- `familia_rito_soito.ged` — só a família Rito, com as notas completas dos assentos (1222 indivíduos)

## Tabelas (pasta `dados/`)
| ficheiro | registos | conteúdo |
|---|---:|---|
| `pessoas_soito.csv` | 2835 | pessoas das genealogias de família, com código, filiação e casamentos |
| `casamentos.csv` | 2387 | assentos de casamento 1730-1972: noivos, idades, filiação, viuvez, testemunhas |
| `batismos.csv` | 3939 | assentos de batismo 1901-1950: datas, pais, quatro avós, padrinhos |
| `obitos.csv` | 2976 | assentos de óbito: data, idade, estado, cônjuge, filiação |
| `familias.csv` | 397 | uniões extraídas das genealogias em prosa |

Tudo gerado por extração automática; erros de transcrição e de leitura são possíveis.

## Leituras dos originais S8

A investigação e as transcrições do blogue **Saber Soito são de Carlos**. As leituras diretas dos originais S8 são uma fonte adicional, visivelmente identificada nas fichas, com ligação ao livro no arquivo.

As entradas manuais estão em `fontes/S8/transcricoes/*.json`; indicam imagem, lado, ordem do assento, excerto e dúvidas. Só `confirmado` entra na árvore. Nascimento desconhecido continua vazio; não se usa a data de batismo como nascimento.

Gerar: `python3 scripts/gerar_assentos_s8.py`. Conferir: `python3 scripts/gerar_assentos_s8.py --check` e `python3 scripts/validar_design.py`. O relatório `dados/assentos_s8_revisao.json` separa leituras pendentes e coincidências de nomes sem fusão. Os resultados da cadeia anterior mantêm-se, pois este checkout não contém todos os parsers necessários para a executar.

## Documentação

- `docs/DESIGN.md` — cores, bordas, tipografia, espaçamento e notação das datas
- `docs/ARCHITECTURE.md` — cadeia de processamento, contratos de dados, estrutura de pastas e publicação
- `docs/CONTEXT.md` — regras de negócio: proveniência, regras genealógicas de ligação, conflitos e pessoas vivas
- `scripts/validar_design.py` — confere `index.html` contra o DESIGN.md; correr antes de publicar
