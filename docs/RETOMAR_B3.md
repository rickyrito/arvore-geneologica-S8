# B3: revisão dirigida concluída até ao fim

Resumo de 21/11/2026. Comunicar em português e poupar contexto. Revisão dirigida concluída até m0122. Continuar no B4 conforme `docs/RETOMAR_B4.md`; não repetir pendentes já revistos sem nova evidência.

## Estado

Repositório `/Users/ricardorito/dev/arvore-geneologica-leve`, branch `main`, origin `https://github.com/rickyrito/arvore-geneologica-S8.git`. Base do lote: `e947d40`; commit pela mensagem «Revê 48 pendentes finais do B2 e 52 do B3».

B2: 930 entradas, 674 confirmadas, 256 pendentes; revisão dirigida chegou ao fim de m0251. Último lote: 48 revistos, sete promovidos, 41 pendentes. Mantêm-se 39 nascimentos explícitos. Avisos anteriores em `docs/RETOMAR_B2.md`.

B3: 453 entradas, 368 confirmadas, 85 pendentes. Primeiro lote dirigido: 52 pendentes revistos até `m0062-e-02`, incluindo continuações necessárias; 14 promovidos e 38 mantidos pendentes. Não há outros alvos antes de m0065 por rever neste percurso. Histórico completo e objetos anteriores em `revisoes` de `fontes/S8/transcricoes/B3-1786-1800.json`. Lote final de 21/11/2026 (base `5ea1174`): 57 revistos de m0065 ao fim, dez confirmados e 47 pendentes. Depois, 43 pendentes do B4 revistos para completar 100. B1, B2, base e todos os confirmados anteriores preservados. Sem nascimentos novos ou ligações de identidade. Dados da aplicação: versão 50.

## Método

Ler apenas pendentes do lote e continuações necessárias nos JPEGs do repositório grande, só de consulta: `/Users/ricardorito/dev/arvore-geneologica-S8/fontes/S8/RegistosDeNascimentos/PT-TT-PRQ-PSBG34-001-B3/PT-ADLSB-PRQ-PSBG34-001-B3_m0065.jpg`. Leitura visual sem OCR. Ampliar e reconferir campos essenciais antes de confirmar; nomes, filiações e datas não são completados pelos avós, margens ou sequência. Não inferir identidades ou apelidos das crianças. Só confirmados entram na aplicação. Preservar hipóteses e dúvidas anteriores.

## Cuidados do lote

- m0008-d-01: Ângela Nunes, corrigida a hipótese provisória Angélica. m0013-d-02 e m0034-d-02: pai José Nunes de Marcos, sem Gonçalves. m0014-e-02: Luciano, sem substituir por Lucas da ascendência.
- m0019-e-01: corpo escreve 1784; mantém-se pendente por ano anterior ao catálogo, rejeitado pela validação atual. Não harmonizar para 1787 nem alargar silenciosamente o catálogo.
- m0025-d-01 permanece pendente por nome materno abreviado; não fixar Maria Francisca. m0032-e-01 conserva Redonda Gonçalves, nome escrito. m0035-e-01: Domingos Antunes.
- m0036-e-02: Domingos digo José; 06/12/1789 é batismo sob condição, não nascimento nem primeiro batismo. m0053-d-01: Maria da Ascensão, original Ascenção, não Assunção. m0055-d-01: Manuel, batismo particular de 11/12/1791; inocente é qualificação marginal, não nome. Óbito sem data inferida.
- m0015-e-02 e m0021-e-02 são redações interrompidas/anuladas; não excluir ou integrar automaticamente. Nomes em branco em m0030-d-03, m0031-e-01 e m0035-e-03. Pai não identificado não origina pai fictício. Óleos sem data do batismo particular continuam pendentes. m0042-d-01 exige esclarecer fórmula, remissão e nome materno.
- m0002 é página única; não cortar artificialmente em duas. m0060 repete m0059. Respeitar inventário e continuações.

## Validação e entrega

Verificar instruções locais e Git; pull antes de editar. Preservar stash antigo, excluir `.DS_Store`. Após o lote: gerar com `python3 scripts/gerar_assentos_s8.py`; atualizar totais do README e cache de dados no HTML. Conferir integridade dos alvos, outros livros, base e confirmados anteriores. Executar gerador `--check`, os testes em `scripts/test_*.py`, `python3 scripts/validar_design.py` e `git diff --check`. Fazer commit e push, acompanhar GitHub Pages (checkout grande pode demorar dez minutos) e verificar uma ficha nova publicada. Atualizar este ponto de retoma.

## Cuidados do lote final

Maria de Rosa (m0071-d-01), Vicenta (m0080-e-01), Brízida (m0104-e-02), Alexandra (m0105-e-01) e Bonifácio (m0113-e-01) reconferidos em ampliação. Em m0108-e-01 o pai é Manuel Martins Jorge. Em m0096-d-02 a mãe é Páscoa Gonçalves Garrida. Em m0106-d-02 conservar batismo de 04/12/1798 e fecho de redação de 14/11/1799, sem harmonizar.

m0067-e-02 e m0102-d-02 continuam pendentes por composição/sintaxe parentais inseguras. m0090-e-02: António Gonçalves Lucas, sem converter óleos em batismo. m0098-d-03 conserva divergência entre 1797 no corpo e 1798 na margem. m0101-d-01 não permite formar casal por inferência. Tinta transpassada limita as últimas páginas. m0122 é página única; o segundo assento tem fecho e assinatura, não é necessariamente truncado. Histórico integral das 57 leituras em `revisoes`.
