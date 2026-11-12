# Genealogia do Soito (Sabugal)

Página: https://rickyrito.github.io/arvore-geneologica-S8/

Dados transcritos dos assentos paroquiais do Soito publicados no blogue [Saber Soito](https://soitoribacoa.blogspot.com/) (294 artigos, 1624-1984).

## Página
- `index.html` + `dados.js` + `dados_s8.js` — explorador: 22 207 pessoas da base e 355 do suplemento S8, com filtros por família e origem. Página não indexada.
- Primeira leitura das 132 imagens do B1 (1692–1705), com segunda revisão visual da secção de batismos, de m0003 até m0064 esquerda, em 12/11/2026: 965 entradas inventariadas, com 128 assentos de campos essenciais confirmados (110 batismos, 11 óbitos e 7 casamentos) e 837 leituras pendentes (314 batismos, 437 óbitos e 86 casamentos). O suplemento contém 117 núcleos; não estabelece identidades com pessoas das genealogias existentes. A revisão chegou ao fim da secção de batismos, mas as leituras pendentes ainda exigem resolução.
- As secções são batismos até m0064 esquerda, óbitos de m0064 direita a m0113 esquerda e casamentos de m0114 direita a m0131 esquerda. Capa, introdução, páginas em branco, visitações e o averbamento posterior de m0132 direita estão identificados nas notas. As fotografias m0027 e m0109 repetem m0026 e m0108 e não geram registos novos. Continuações entre páginas também não são contadas de novo.
- A leitura é parcial, com excertos e dúvidas guardados; não é transcrição diplomática integral. Rasgos, manchas, tinta transpassada e algumas delimitações de assentos exigem revisão. Os anos são conferidos no texto, sem os inferir pela sequência das imagens. Cerimónias de santos óleos com data de batismo incerta ficam pendentes.

O GitHub Pages exclui `fontes/` através de `_config.yml`; as imagens e transcrições continuam guardadas no repositório. O explorador mantém as ligações ao arquivo.

## GEDCOM
- `familia_soito.ged` — base anterior da freguesia: 22 207 indivíduos, 9253 núcleos familiares
- `assentos_s8.ged` — suplemento de originais S8: 355 indivíduos, 117 núcleos; não está incluído no GEDCOM anterior
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

As entradas manuais estão em `fontes/S8/transcricoes/*.json`; indicam imagem, lado, ordem do assento, excerto e dúvidas. Só `confirmado` entra na árvore. Nascimento desconhecido continua vazio; não se usa a data de batismo ou uma idade para o calcular. Sepultura não é tratada como data de óbito. Nos óbitos e casamentos, parentes apenas mencionados nos excertos não originam novas ligações nesta primeira leitura.

Gerar: `python3 scripts/gerar_assentos_s8.py`. Conferir: `python3 scripts/gerar_assentos_s8.py --check`, `python3 -m unittest discover -s scripts -p 'test_*.py'` e `python3 scripts/validar_design.py`. O relatório `dados/assentos_s8_revisao.json` separa leituras pendentes e coincidências de nomes sem fusão. Os resultados da cadeia anterior mantêm-se, pois este checkout não contém todos os parsers necessários para a executar.

## Documentação

- `docs/DESIGN.md` — cores, bordas, tipografia, espaçamento e notação das datas
- `docs/ARCHITECTURE.md` — cadeia de processamento, contratos de dados, estrutura de pastas e publicação
- `docs/CONTEXT.md` — regras de negócio: proveniência, regras genealógicas de ligação, conflitos e pessoas vivas
- `scripts/validar_design.py` — confere `index.html` contra o DESIGN.md; correr antes de publicar
