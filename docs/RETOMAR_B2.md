# Retomar a revisão do B2 na m0061

Resumo de 19/11/2026. Continuar a revisão visual dos assentos pendentes do B2 a partir de m0061, por lotes de cerca de 20 imagens. Atualizar as transcrições e a aplicação; validar, fazer commit e push no final do lote. Comunicar em português, com respostas curtas.

## Caminhos

- Trabalhar em `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`.
- Ler JPEGs em `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B2/`. Padrão: `PT-ADLSB-PRQ-PSBG34-001-B2_m0061.jpg`.
- Editar `fontes/S8/transcricoes/B2-1728-1759.json` na cópia leve. O repositório grande serve apenas para consultar imagens.

## Estado confirmado

Base deste lote: `df88a97` (main). Leitura inicial das 251 imagens do B2 concluída: 930 entradas, agora 626 confirmadas e 304 pendentes. Revisões dirigidas: até m0020, 29 revistos (5 promovidos); m0021–m0040, 15 revistos (3 promovidos); m0041–m0060, 48 revistos (16 promovidos e 32 ainda pendentes). Histórico completo em `revisoes`; base, B1, B3, B4 e confirmados anteriores preservados. Consultar o commit deste lote pela mensagem «Revê 48 pendentes do B2 entre m0041 e m0060».

Próximo: `S8-B2-m0061-e-01`. Continuar pelos pendentes de m0061–m0080. Não repetir os pendentes dos lotes anteriores sem nova evidência. O B2 tem 39 datas explícitas de nascimento estruturadas; neste lote acrescentou-se Luís em m0042-e-01 (27/08/1734; batismo 08/09/1734). Carrilho confirmado visualmente em m0042 e m0058 sem ligar identidades. Em m0059-e-01, a emenda «digo filho de» distingue os pais Manuel de Carvalho e Maria João dos avós; batismo 24/09/1738, redação 07/11/1738. A remissão ambígua de m0059-e-02 continua pendente. m0060-e-03 e m0060-d-01 registam santos óleos sem data explícita segura do batismo anterior.

Neste lote: 16 confirmados; 32 pendentes com dúvidas específicas. Menções a santos óleos dentro da fórmula «batizei solenemente e pus os santos óleos» não foram confundidas com cerimónias posteriores a batismo particular. Nomes adicionais, emendas e anos divergentes conservam-se no histórico. Validações concluídas sem erros: gerador, --check, 11 testes, design e diff. Publicação pelo GitHub Pages pode demorar no checkout do repositório grande (cerca de 20 GB); acompanhar a execução antes de verificar uma ficha nova.

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
