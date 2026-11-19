# Retomar a revisão do B2 na m0041

Resumo de 19/11/2026. Continuar a revisão visual dos assentos pendentes do B2 a partir de m0041, por lotes de cerca de 20 imagens. Atualizar as transcrições e a aplicação; validar, fazer commit e push no final do lote. Comunicar em português, com respostas curtas.

## Caminhos

- Trabalhar em `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`.
- Ler JPEGs em `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B2/`. Padrão: `PT-ADLSB-PRQ-PSBG34-001-B2_m0041.jpg`.
- Editar `fontes/S8/transcricoes/B2-1728-1759.json` na cópia leve. O repositório grande serve apenas para consultar imagens.

## Estado confirmado

Base recebida por pull: `df30ee2` (inclui B3 e B4; preservar). Leitura inicial das 251 imagens do B2 concluída: 930 entradas, agora 610 confirmadas e 320 pendentes. Revisão até m0020: 29 revistos, cinco promovidos e 24 ainda pendentes. Em 19/11 foram revistos os 15 pendentes de m0021–m0040: três promovidos (m0022-d-02, m0030-d-02, m0037-d-01), doze mantêm dúvidas. Histórico completo em `revisoes`; B1, B3, B4 e confirmados anteriores preservados. O commit deste lote pode ser consultado no Git pela mensagem «Revê 15 pendentes do B2 entre m0021 e m0040».

Próximo: `S8-B2-m0041-e-01`. Continuar pelos pendentes de m0041–m0060. Não repetir os doze pendentes deste lote sem nova evidência. m0021 mantém a designação do pai insegura, embora a abertura tenha sido relida como 27/03/1731. O B2 tem agora 38 datas explícitas de nascimento estruturadas; a nova é de Francisco em m0030-d-02, cujo batismo é referido como ocorrido «em os ditos dias», sem se corroborar a antiga hipótese de batismo em casa.

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
