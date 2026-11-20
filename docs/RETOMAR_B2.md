# Retomar a revisão do B2 na m0182

Resumo de 20/11/2026. Continuar a revisão visual dos assentos pendentes do B2 a partir de m0182, por lotes de cerca de 20 imagens. Atualizar as transcrições e a aplicação; validar, fazer commit e push no final do lote. Comunicar em português, com respostas curtas.

## Caminhos

- Trabalhar em `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`.
- Ler JPEGs em `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B2/`. Padrão: `PT-ADLSB-PRQ-PSBG34-001-B2_m0182.jpg`.
- Editar `fontes/S8/transcricoes/B2-1728-1759.json` na cópia leve. O repositório grande serve apenas para consultar imagens.

## Estado confirmado

Base deste lote: `d904cdd` (main). B2: 930 entradas inventariadas, 667 confirmadas e 263 pendentes; mantêm-se 39 datas explícitas de nascimento. Leitura inicial das 251 imagens concluída. Revisões dirigidas: até m0020, 29 revistos (5 promovidos); m0021–m0040, 15 (3); m0041–m0060, 48 (16); m0061–m0080, 60 (14); m0081–m0100, 35 (8); m0101–m0180, 93 (19 promovidos e 74 ainda pendentes). Histórico completo em `revisoes`; base, B1, B3, B4 e os 648 confirmados anteriores preservados. Consultar o commit deste lote pela mensagem «Revê 93 pendentes do B2 entre m0101 e m0180».

Próximo: `S8-B2-m0182-e-02`. Continuar pelos pendentes de m0181–m0200 (não há pendentes em m0181). Não repetir os lotes anteriores sem nova evidência. O intervalo até m0180 foi revisto integralmente quanto aos 93 pendentes, incluindo continuações necessárias até m0180 direita; m0181 esquerda foi consultada para verificar a transição. m0114-d-02: Maria, filha de Manuel Martins Pedrado e Teresa Fernandes, 26/12/1744 (vinte e seis, em vez de vinte e cinco). m0176-d-02: Vitória, filha de Manuel Nunes da Torre e Leonor Gonçalves, 23/12/1751; o corpo corrige expressamente Leonor Fernandes para Gonçalves. Conservados os anos individuais 1744 (m0144-d-02 e m0147-d-02), 1746 (m0115-e-01, m0117-e-01, m0118-e-01/d-01, m0136-e-01, m0141-e-01/e-03) e 1750 em m0147-d-03, sem harmonizar pela sequência.

Atenção futura: m0150-e-01 (Manuel e António), m0151-d-01 (Isabel e Ana) e m0174-e-02 (Domingos e Isabel) são termos conjuntos de gémeos, conservados pendentes até representação individual segura; não fundir crianças nem duplicar termos. m0158-e-01 contém José de Carvalho e depois dito João de Carvalho; m0157-d-02 tem filiação corrigida que diverge da ascendência. m0178-d-02 admite mãe Ana Afonso em vez de Ana Nunes, ainda pendente. m0138-d-01 tem possível inversão dos dias do batismo particular e óleos; m0173-d-02 emenda agosto para último de julho, condicionando a remissão de m0174-e-01. m0123-e-01 é justificação de adulto, sem calcular data pela idade; m0140-e-01 é certidão de batismo antigo, sem usar 1747 da justificação. Muitos óleos permanecem sem data do batismo particular.

Aviso anterior preservado: m0087-d-01 e d-02 parecem sobrepor-se ao único assento autónomo de Manuel na página direita; ambas pendentes, sem exclusões nem dois batismos confirmados. m0095-e-01 tem fórmula e filiação materna incertas; m0094-e-01 admite Eustácia/Eustáquia. Tinta transpassada limita muitos campos. Não inferir datas do batismo particular pelos óleos, nem nomes pelos avós/margens. Sem ligações de identidade nem nascimentos inferidos.

Validações concluídas: gerador, --check, 11 testes, design e diff; integridade dos 93 alvos, base, outros livros e confirmados anteriores conferida. Publicação pelo GitHub Pages pode demorar cerca de 10 minutos no checkout do repositório grande; acompanhar antes de conferir uma ficha nova. Dados da aplicação: versão 48.

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
