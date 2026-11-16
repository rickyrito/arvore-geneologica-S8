# Genealogia do Soito (Sabugal)

Página: https://rickyrito.github.io/arvore-geneologica-S8/

Dados transcritos dos assentos paroquiais do Soito publicados no blogue [Saber Soito](https://soitoribacoa.blogspot.com/) (294 artigos, 1624-1984).

## Página
- `index.html` + `dados.js` + `dados_s8.js` — explorador: 22 207 pessoas da base e 2776 do suplemento S8, com filtros por família e origem. Página não indexada.
- Primeira leitura das 132 imagens do B1 (1692–1705), com segunda revisão visual concluída até m0132 inclusive, em 12/11/2026: 965 entradas inventariadas, com 213 assentos de campos essenciais confirmados (110 batismos, 61 óbitos e 42 casamentos) e 752 leituras pendentes (314 batismos, 387 óbitos e 51 casamentos). Os assentos do B1 correspondem a 152 núcleos; não estabelece identidades com pessoas das genealogias existentes. A segunda revisão chegou ao fim do B1, que termina em m0132; as leituras pendentes ainda exigem resolução. A continuação passa para o B2 (1728–1759), com numeração própria a partir de m0001.
- B2 (catálogo: 1728–1759): leitura de m0001 a m0251 inclusive, com 930 entradas inventariadas; 607 batismos com campos essenciais confirmados e 323 leituras pendentes. Todas as 251 imagens percorridas; leitura inicial do livro concluída, mantendo os assentos pendentes para revisão. Mantêm-se 37 datas de nascimento explicitamente indicadas e guardadas separadamente do batismo. O lote m0241–m0251 acrescenta 37 entradas: 27 confirmadas em duas leituras visuais e 10 pendentes. Santos óleos sem data do batismo e redação posterior ficam distinguidos nas notas; continuações entre páginas não são duplicadas. As correções da segunda leitura conservam a hipótese inicial. A grafia sinco nas aberturas de janeiro a março foi conferida em ampliação como cinco (1745), sem dedução pela sequência. Conserva-se o ano escrito de 1740 num batismo entre registos de 1741; o ano de outro batismo reposto em 1741 continua pendente. O livro contém também reposições de batismos anteriores a 1728, descritas com a divergência e ainda pendentes. Em 16/11/2026 foram revistas as 29 leituras pendentes até m0020: cinco passaram a confirmadas e 24 conservam dúvidas específicas; hipóteses e dúvidas iniciais ficaram preservadas no histórico. No conjunto B1+B2: 1895 entradas, 820 confirmadas e 1075 pendentes; 2296 pessoas e 759 núcleos no suplemento.
- B3 (catálogo: 1786–1800; 122 imagens): leitura de m0001 a m0050 inclusive, em 16/11/2026, com 206 entradas inventariadas; 160 batismos com campos essenciais confirmados em duas leituras visuais e 46 leituras pendentes. Próxima imagem: m0051; apenas o seu topo foi consultado para concluir a entrada iniciada em m0050. Os lotes m0031–m0050 acrescentaram 83 entradas, 67 confirmadas e 16 pendentes. As menções adicionais de avós, padrinhos e naturalidades são provisórias e conservadas nas leituras iniciais. Santos óleos sem data do batismo, redações interrompidas/canceladas, nomes não preenchidos e um ano lido 1784 anterior ao intervalo do catálogo ficam pendentes. Conservam-se os anos escritos, incluindo 1789 de m0017 direita e dezembro de 1789 de m0030 direita, apesar dos assentos vizinhos. A placa «erro de numeração» em m0026 foi assinalada sem alterar a ordem das imagens do arquivo. As datas dos batismos particulares de 26/08/1790 e 15/08/1791 foram distinguidas das cerimónias posteriores de santos óleos, de 27/08/1790 e 20/08/1791. Averbamentos posteriores ficam assinalados sem eventos inferidos; a menção de falecimento antes dos santos óleos em m0050 esquerda não fornece uma data exata de óbito. Não foram confirmadas novas datas de nascimento nestes lotes. No conjunto B1+B2+B3: 2101 entradas, 980 confirmadas e 1121 pendentes; 2776 pessoas e 919 núcleos no suplemento.
- No B1, as secções são batismos até m0064 esquerda, óbitos de m0064 direita a m0113 esquerda e casamentos de m0114 direita a m0131 esquerda. Capa, introdução, páginas em branco, visitações e o averbamento posterior de m0132 direita estão identificados nas notas. As fotografias m0027 e m0109 repetem m0026 e m0108 e não geram registos novos. Continuações entre páginas também não são contadas de novo.
- A leitura é parcial, com excertos e dúvidas guardados; não é transcrição diplomática integral. Rasgos, manchas, tinta transpassada e algumas delimitações de assentos exigem revisão. Os anos são conferidos no texto, sem os inferir pela sequência das imagens. Cerimónias de santos óleos com data de batismo incerta ficam pendentes.

O GitHub Pages exclui `fontes/` através de `_config.yml`; as imagens e transcrições continuam guardadas no repositório. O explorador mantém as ligações ao arquivo.

## GEDCOM
- `familia_soito.ged` — base anterior da freguesia: 22 207 indivíduos, 9253 núcleos familiares
- `assentos_s8.ged` — suplemento de originais S8: 2776 indivíduos, 919 núcleos; não está incluído no GEDCOM anterior
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

As entradas manuais estão em `fontes/S8/transcricoes/*.json`; indicam imagem, lado, ordem do assento, excerto e dúvidas. Só `confirmado` entra na árvore. Nascimento explicitamente indicado no original é guardado separadamente, com evidência e validação cronológica. Nascimento desconhecido continua vazio; não se usa a data de batismo ou uma idade para o calcular. Sepultura não é tratada como data de óbito. Nos óbitos e casamentos, parentes apenas mencionados nos excertos não originam novas ligações nesta primeira leitura.

Gerar: `python3 scripts/gerar_assentos_s8.py`. Conferir: `python3 scripts/gerar_assentos_s8.py --check`, `python3 -m unittest discover -s scripts -p 'test_*.py'` e `python3 scripts/validar_design.py`. O relatório `dados/assentos_s8_revisao.json` separa leituras pendentes e coincidências de nomes sem fusão. Os resultados da cadeia anterior mantêm-se, pois este checkout não contém todos os parsers necessários para a executar.

## Documentação

- `docs/DESIGN.md` — cores, bordas, tipografia, espaçamento e notação das datas
- `docs/ARCHITECTURE.md` — cadeia de processamento, contratos de dados, estrutura de pastas e publicação
- `docs/CONTEXT.md` — regras de negócio: proveniência, regras genealógicas de ligação, conflitos e pessoas vivas
- `scripts/validar_design.py` — confere `index.html` contra o DESIGN.md; correr antes de publicar
