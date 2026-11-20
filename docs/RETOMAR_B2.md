# Retomar a revisão do B2 na m0081

Resumo de 20/11/2026. Continuar a revisão visual dos assentos pendentes do B2 a partir de m0081, por lotes de cerca de 20 imagens. Atualizar as transcrições e a aplicação; validar, fazer commit e push no final do lote. Comunicar em português, com respostas curtas.

## Caminhos

- Trabalhar em `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`.
- Ler JPEGs em `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B2/`. Padrão: `PT-ADLSB-PRQ-PSBG34-001-B2_m0081.jpg`.
- Editar `fontes/S8/transcricoes/B2-1728-1759.json` na cópia leve. O repositório grande serve apenas para consultar imagens.

## Estado confirmado

Base deste lote: `50d3a51` (main). B2: 930 entradas, 640 confirmadas e 290 pendentes; mantêm-se 39 datas explícitas de nascimento. Leitura inicial das 251 imagens concluída. Revisões dirigidas: até m0020, 29 revistos (5 promovidos); m0021–m0040, 15 revistos (3 promovidos); m0041–m0060, 48 revistos (16 promovidos); m0061–m0080, 60 revistos (14 promovidos e 46 ainda pendentes). Histórico completo em `revisoes`; base, B1, B3, B4 e os 626 confirmados anteriores preservados. Consultar o commit deste lote pela mensagem «Revê 60 pendentes do B2 entre m0061 e m0080».

Próximo: `S8-B2-m0081-e-01`. Continuar pelos pendentes de m0081–m0100. Não repetir os lotes anteriores sem nova evidência. Neste lote, a ampliação confirmou Isabel Fernandes como mãe de Domingos (m0064-d-02), substituindo a hipótese Lourença. A reposição de Maria (m0075-d-03) refere batismo em 24/01/1734 pelo padre Francisco Barrela e redação em 12/04/1741. Em m0071-e-03, Ana é filha de Manuel Pires e Josefa Martins, batismo por remissão de 07/08/1740. Em m0074-d-02, Catarina é filha de Domingos Nabais e Maria Pinto, batismo por remissão de 10/03/1741. As fórmulas «solenemente batizei e pus os santos óleos» foram distinguidas dos óleos posteriores a batismo em casa, cuja data continua pendente quando não explícita. Divergências de nomes e anos permanecem no histórico; sem ligações de identidade nem nascimentos inferidos.

Validação do lote: gerador, --check, 11 testes, design e diff. Publicação pelo GitHub Pages pode demorar no checkout do repositório grande (cerca de 20 GB); acompanhar a execução antes de verificar uma ficha nova.

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
