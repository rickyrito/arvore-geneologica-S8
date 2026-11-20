# Retomar a revisão do B2 na m0101

Resumo de 20/11/2026. Continuar a revisão visual dos assentos pendentes do B2 a partir de m0101, por lotes de cerca de 20 imagens. Atualizar as transcrições e a aplicação; validar, fazer commit e push no final do lote. Comunicar em português, com respostas curtas.

## Caminhos

- Trabalhar em `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`.
- Ler JPEGs em `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B2/`. Padrão: `PT-ADLSB-PRQ-PSBG34-001-B2_m0101.jpg`.
- Editar `fontes/S8/transcricoes/B2-1728-1759.json` na cópia leve. O repositório grande serve apenas para consultar imagens.

## Estado confirmado

Base deste lote: `9d8eb9e` (main). B2: 930 entradas inventariadas, 648 confirmadas e 282 pendentes; mantêm-se 39 datas explícitas de nascimento. Leitura inicial das 251 imagens concluída. Revisões dirigidas: até m0020, 29 revistos (5 promovidos); m0021–m0040, 15 revistos (3); m0041–m0060, 48 revistos (16); m0061–m0080, 60 revistos (14); m0081–m0100, 35 revistos (8 promovidos e 27 ainda pendentes). Histórico completo em `revisoes`; base, B1, B3, B4 e os 640 confirmados anteriores preservados. Consultar o commit deste lote pela mensagem «Revê 35 pendentes do B2 entre m0081 e m0100».

Próximo: `S8-B2-m0101-d-02`. Continuar pelos pendentes de m0101–m0120. Não repetir os lotes anteriores sem nova evidência. A continuação de m0100-d-02 em m0101 esquerda foi lida: António, filho de Luís Carrilho e Isabel Nabais, batismo 06/01/1744 (corrige a hipótese Luís, filho de António Carrilho). Em m0082-e-03, Maria é filha de Manuel Nunes e Ana Marques, batismo 05/06/1742 (cinco, não quinze); em m0083-d-02, Maria é filha de Sebastião Rodrigues e Catarina Antunes, batismo 19/08/1742 (dezanove, não vinte). Remissão de m0082-e-01 resolvida para 12/05/1742, sem promover o assento anterior cuja mãe está manchada.

Atenção futura: m0087-d-01 e d-02 parecem sobrepor-se ao único assento autónomo de Manuel visível na página direita, após continuação de Francisco. Ambas mantidas pendentes, com dúvida de delimitação explícita; não foram excluídas nem contadas como dois batismos confirmados. Em m0095-e-01, a ampliação admite «batizei solenemente e pus os santos óleos», divergindo da classificação inicial como apenas óleos; fórmula e filiação materna continuam pendentes. Em m0094-e-01, nome da criança admite Eustácia/Eustáquia em vez de Anastácia, ainda pendente. Tinta transpassada limita muitos campos. Não inferir datas do batismo particular a partir dos óleos, nem nomes pelos avós/margens. Sem ligações de identidade nem nascimentos inferidos.

Validações do lote: gerador, --check, 11 testes, design e diff. Publicação pelo GitHub Pages pode demorar cerca de 10 minutos no checkout do repositório grande; acompanhar antes de conferir uma ficha nova.

## Leitura e poupança de contexto

- Consultar apenas os pendentes do lote e as continuações necessárias. Ampliar campos duvidosos, preservando legibilidade; leitura visual sem OCR.
- Confirmar nome, sexo, filiação e data do batismo no original. Conservar leituras anteriores e dúvidas em `revisoes`, seguindo o último exemplo do JSON.
- Dúvidas permanecem pendentes. Distinguir batismo, santos óleos, redação e reposição. Nascimento só com evidência explícita; conservar divergências cronológicas.
- Não deduzir apelidos, datas ou identidades com o blogue. Só `confirmado` entra na aplicação; preservar a base e os confirmados anteriores.
- Usar scripts para validações e geração; evitar reler ficheiros gerados inteiros. Guardar o próximo ponto neste resumo ao terminar.

## Retoma e entrega

1. Verificar instruções locais e estado Git; fazer pull antes de editar, preservando trabalho existente. Manter `.DS_Store` fora do commit e conservar o stash antigo de leitura local sem o aplicar.
2. Após a revisão, executar `python3 scripts/gerar_assentos_s8.py`, atualizar os totais do README e incrementar a versão de `dados_s8.js` no HTML se os dados mudarem.
3. Validar com `python3 scripts/gerar_assentos_s8.py --check`, `python3 -m unittest discover -s scripts -p 'test_*.py'`, `python3 scripts/validar_design.py` e `git diff --check`.
4. Conferir o diff, fazer commit e push, aguardar publicação e verificar uma ficha alterada em https://rickyrito.github.io/arvore-geneologica-S8/.

Detalhes de implementação: consultar apenas as secções necessárias de `docs/ARCHITECTURE.md`. Os antigos ficheiros temporários de revisão já não estão disponíveis.
