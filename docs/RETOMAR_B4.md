# Retomar a revisão do B4 na m0040

Resumo de 21/11/2026. Comunicar em português e poupar contexto. Continuar a revisão dirigida pelos pendentes a partir de `S8-B4-m0040-e-01`. Não repetir os primeiros 43 sem nova evidência. Esta retoma é da revisão de pendentes; a leitura inicial do livro só chegou a m0100, tendo m0101 como próxima imagem ainda não inventariada.

## Estado

Repositório `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`. Base do lote: `5ea1174`; commit pela mensagem «Revê 57 pendentes finais do B3 e 43 do B4».

B3: revisão dirigida concluída até ao fim, 453 entradas, 368 confirmadas e 85 pendentes. Cuidados em `docs/RETOMAR_B3.md`. B4: 440 entradas inventariadas em m0001–m0100, 312 confirmadas e 128 pendentes. Primeiro lote dirigido do B4: 43 revistos até `m0037-e-01`, sete promovidos e 36 mantidos pendentes. Com os 57 do B3 foram revistos 100 assentos neste lote. Sem nascimentos novos ou ligações de identidade. Confirmados anteriores, B1, B2 e base preservados. Dados da aplicação: versão 50.

Histórico completo com os objetos anteriores em `revisoes` de `fontes/S8/transcricoes/B4-1803-1854.json`. Todos os pendentes anteriores a m0040 já foram revistos neste percurso.

## Método

Ler apenas pendentes do lote e continuações necessárias nos JPEGs do repositório grande, só de consulta: `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B4/PT-TT-PRQ-PSBG34-001-B4_m0040.jpg`. Atenção ao prefixo PT-TT no B4, diferente do PT-ADLSB no B3. Leitura visual sem OCR. Ampliar e reconferir campos essenciais antes de confirmar. Não completar nomes ou datas pelos avós, margens ou sequência; não inferir identidades ou apelidos das crianças. Só confirmados entram na aplicação. Preservar hipóteses e dúvidas anteriores.

## Cuidados deste lote

- m0002 é página única, com fragmentos mutilados; não dividir artificialmente. m0009 repete m0008.
- Confirmados: m0005-d-02 Domingos, 04/04/1804 (quatro, corrigindo catorze); m0010-e-01 Manuel, Sebastião Costa Pires/Luísa Gonçalves; m0012-d-02 Maria, Manuel Martins Antunes/Maria Martins Garrida; m0015-d-01 Maria, António Martins Fernandes/Rosa Lourença; m0016-e-01 Ana, José Esteves Nunes/Ana Dias; m0019-d-02 Maria, Domingos Pereira/Catarina Martins (sem Viegas); m0026-e-02 Bárbara, José Rodrigues/Maria Nunes. Notas individuais seguem para o GEDCOM.
- m0013-d-02 conserva dúvida 1805/1806. m0015-e-01 e e-02 são óleos sem data segura do batismo particular. m0016-d-02: Maria, Isabel Gonçalves solteira, sem pai declarado; leitura de 07/08/1805 por remissão segura, mas integração atual exige ambos os pais. Não inventar pai ou alterar o modelo silenciosamente.
- m0023-e-02: melhor leitura sete de junho, antes julho, filiação ainda pendente. m0027-d-03: Maria exposta, batismo sob condição; Manuel Jorge/Luísa Martins são o casal da porta, não pais. Continuação m0028-e consultada.
- m0031-e-02 nome Luísa/Lúcia emendado; m0033-d-01 nome materno e alcance de exposta inseguros; m0035-e-02 admite Alexandra no corpo, além de Josefa/Joana anteriores, sem fixar. m0037-e-01 é redação interrompida; não fundir com a Ana seguinte da página direita.
- Manchas e tinta transpassada impedem várias filiações. Preservar as dúvidas específicas; confirmação não é quota.

## Validação e entrega

Verificar instruções locais e Git; pull antes de editar. Preservar stash antigo, excluir `.DS_Store`. Gerar com `python3 scripts/gerar_assentos_s8.py`; atualizar totais do README e cache de dados no HTML. Conferir integridade dos alvos, outros livros, base e confirmados anteriores. Executar gerador `--check`, testes `python3 -m unittest discover -s scripts -p 'test_*.py'`, `python3 scripts/validar_design.py` e `git diff --check`. Fazer commit e push, acompanhar GitHub Pages (checkout grande pode demorar dez minutos) e verificar uma ficha nova publicada. Atualizar o ponto de retoma.
