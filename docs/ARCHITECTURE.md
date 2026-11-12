# ARCHITECTURE.md — Árvore Genealógica, Família Rito do Soito

Descreve o que está implementado. Nenhum componente ou script novo introduz padrões fora
daqui sem alterar primeiro este ficheiro.

---

## 1. Natureza do projeto

Não é uma aplicação com servidor. São duas coisas:

1. **Uma cadeia de extração**, em Python, que lê o arquivo do blogue *Saber Soito* e produz
   tabelas e um GEDCOM.
2. **Uma página estática**, um único HTML com um ficheiro de dados ao lado, publicada em
   GitHub Pages e como artefacto privado.

Não há base de dados, nem API, nem build. O estado vive em ficheiros.

---

## 2. Pastas

```
/                     index.html      página (HTML, CSS e JS num só ficheiro)
                      dados.js        dados da árvore, gerados; nunca editados à mão
                      familia_soito.ged        GEDCOM da freguesia
                      familia_rito_soito.ged   GEDCOM só da família Rito
                      README.md
/docs                 DESIGN.md, ARCHITECTURE.md, CONTEXT.md
/dados                CSV gerados: pessoas, casamentos, batismos, óbitos,
                      duplicados, suspeitas, conflitos_registos,
                      acrescentos_aplicados
                      CSV mantido à mão: acrescentos_carlos
```

Regra: tudo em `/dados` e `dados.js` é **gerado**. Corrige-se o parser e volta-se a gerar;
não se edita o resultado.

Exceção para correções da base existente: `dados/acrescentos_carlos.csv`. É o ficheiro de entrada da informação que
não vem do blogue — o que o autor da investigação enviou por email e o que se leu em
assentos fotografados. Escreve-se à mão, cada linha leva a sua fonte, e o passo 12 aplica-o.

---

## 3. Cadeia de processamento

Ordem fixa. Cada etapa lê ficheiros da anterior e escreve os seus.

| # | Script | Entrada | Saída |
|---|---|---|---|
| 1 | `parse_cas2.py` | arquivo do blogue (JSON) | `casamentos.csv` |
| 2 | `parse_bat2.py` | arquivo do blogue | `batismos.csv` |
| 3 | `parse_obi.py` | arquivo do blogue | `obitos.csv` |
| 4 | `parse_fam2.py` | genealogias com códigos | `pessoas_familias.csv` |
| 5 | `parse_prosa.py` | genealogias em prosa | `familias_prosa.csv` |
| 6 | `merge_base.py` | 4 + base Rito detalhada | `pessoas_soito.csv` |
| 7 | `gerar3.py` | 6 | `dados_completo.json` |
| 8 | `fundir.py` | 7 | `dados_fundido.json`, `duplicados.csv` |
| 9 | `fusao_registos.py` | 8 + 1,2,3,5 | `dados_registos.json`, `conflitos_registos.csv` |
| 10 | `fundir2.py` | 9 | `dados_final.json` (+ duplicados) |
| 11 | `limpar.py` | 10 | `dados_final.json` limpo, `suspeitas.csv` |
| 12 | `aplicar_acrescentos.py` | 11 + `dados/acrescentos_carlos.csv` | `dados_final.json`, `acrescentos_aplicados.csv` |
| 13 | `ged_final.py` | 12 | `familia_soito.ged`, `dados.js` |

O passo 9 liga cada assento à pessoa certa por três regras, e não só pelo nome:

- **Ordem cronológica.** Batismos e óbitos são lidos por data real, não pela ordem do
  ficheiro — um assento só se lê depois dos que o antecedem.
- **Ligação pela filiação.** Antes de criar pessoa nova, procura-se entre os filhos já
  ligados ao casal um com o mesmo nome próprio e datas compatíveis. É o que apanha a
  criança que a genealogia regista com apelido e o assento regista só pelo nome próprio.
- **Óbito de criança liga pela idade.** Com idade declarada («8 meses») e filiação,
  calcula-se a data de nascimento implícita e liga-se ao filho do casal cuja data bate
  dentro da margem (10 dias se a idade vier em dias, 45 se vier em meses, 400 se em anos).

Correr a cadeia inteira é a forma normal de aplicar qualquer correção; não há atalhos por
etapas isoladas, porque as fusões dependem do que veio antes.

---

### 3.1. Leituras diretas dos originais S8

O checkout atual não contém os parsers iniciais nem `ged_final.py`/`dados_final.json`
necessários para executar os treze passos. Não se reconstrói essa base por adivinhação.
As novas leituras têm uma cadeia aditiva independente, sem alterar os resultados do blogue:

1. `fontes/S8/transcricoes/*.json` é entrada manual revista, com livro, imagem, lado,
   posição, excerto, campos essenciais e dúvidas. É a segunda exceção de entrada manual,
   fora de `/dados`. `confirmado` significa leitura dos campos essenciais; não significa
   transcrição diplomática integral nem identidade comprovada com uma pessoa do blogue.
2. `python3 scripts/gerar_assentos_s8.py` valida as entradas e gera `dados_s8.js`,
   `assentos_s8.ged` e `dados/assentos_s8_revisao.json`. `--check` verifica estes resultados
   sem os escrever. Só assentos `confirmado` entram na árvore e no GEDCOM suplementar;
   leituras `pendente` ficam apenas no relatório de revisão.
3. A página carrega `dados.js` e depois `dados_s8.js?v=N`, antes do seu próprio script.
   O segundo ficheiro acrescenta pessoas e famílias a `window.ARVORE`, ajustando os índices
   relativos pelo tamanho da base. Não altera pessoas, famílias ou índices anteriores.
   `window.ARVORE.assentosS8` guarda os IDs aplicados e impede aplicação dupla.
4. Não há fusão automática por nome, mesmo para casais. Coincidências com casais da base
   vão para o relatório, sem estabelecer parentesco. Cada pessoa nova tem fonte e papel
   no assento. Não se copia a data de batismo para nascimento nem se atribui apelido ao bebé.
5. `assentos_s8.ged` contém apenas o suplemento de originais, sem substituir o GEDCOM da
   base. Os relatórios anteriores mantêm-se. Quando a cadeia completa voltar a estar
   disponível, a reconciliação terá de ser explícita para evitar duplicar estes assentos.

6. Repetições de fotografias ficam em `imagens_duplicadas` na entrada manual, com
   `imagem`, `repete` (imagem canónica) e `motivo`. Ambas têm de constar do inventário
   e das imagens examinadas. Não se admitem assentos na fotografia repetida, nem
   referências circulares ou a outra repetida. A fotografia alternativa continua
   disponível para apoio de leitura. O relatório gerado conserva esta lista e
   as `notas_pagina`, incluindo continuações e notas de visitação.

7. `tipo` distingue `batismo` (valor por omissão para as entradas anteriores), `obito`
   e `casamento`. Cada confirmação exige excerto e os campos essenciais do evento:
   batismo com criança, sexo, pais e `data_batismo`; óbito com `falecido` (nome e sexo,
   que pode ser vazio quando não explícito) e pelo menos `data_obito` ou `data_sepultura`;
   casamento com `noivo`, `noiva` e `data_casamento`. Todas as datas são explícitas e
   validadas no intervalo do livro, salvo o nascimento explícito descrito abaixo.
   Uma remissão só pode usar um evento confirmado
   do mesmo tipo e com a mesma data; no óbito, refere especificamente `data_obito`.
8. Um óbito cria uma pessoa independente: apenas `data_obito` ocupa a data de óbito
   da ficha. `data_sepultura` conserva-se na fonte, evidência e evento GEDCOM `BURI`,
   sem inferir a morte ou o nascimento. Um casamento cria dois nubentes e um núcleo
   com data, sem filhos ou pais inferidos. Parentes apenas mencionados nos excertos
   não geram ligações nesta primeira leitura. Mantém-se a ausência de fusão automática.
   No GEDCOM, cada pessoa e casamento apontam para a fonte do respetivo assento,
   independentemente do número de pessoas criadas. O relatório inclui totais por tipo.

9. Um batismo pode incluir `data_nascimento` apenas com `evidencia_nascimento` explícita
   no original. A data tem de ser válida e não posterior ao batismo; pode anteceder
   o intervalo do livro. É guardada no campo de nascimento e no evento GEDCOM `BIRT`,
   separadamente de `BAPM`. Não se calcula por idade nem se copia do batismo.
10. Os caminhos relativos das imagens nas evidências, relatório e GEDCOM usam sempre
    separadores `/` (POSIX), também quando o gerador corre em Windows. A geração
    deve produzir os mesmos ficheiros em ambos os sistemas.

O filtro «Assentos originais S8» permite consultar este suplemento. As fontes incluem uma
ligação ao livro no arquivo. A versão `?v=N` de `dados_s8.js` sobe quando este muda.


## 4. Contratos de dados

### CSV
Cabeçalho na primeira linha, UTF-8, vírgula, nomes de coluna em minúsculas sem acentos nas
tabelas geradas (`pai_noivo`, `mae_noiva`, `avos_paternos`). Datas em `DD/MM/AAAA` nos CSV —
a apresentação em `DD-MM-AAAA` é só da página. Data aproximada: `c.AAAA`.

### `dados.js`
Um único `window.ARVORE = {p: [...], f: [...]}`. Arrays posicionais, para o ficheiro ser
pequeno. **A ordem dos campos é contrato**; acrescentam-se campos no fim, nunca no meio.

Pessoa `p[i]`:

| índice | campo |
|---|---|
| 0 | nome |
| 1 | sexo (`M`, `F` ou vazio) |
| 2 | nascimento |
| 3 | batismo |
| 4 | óbito |
| 5 | código do blogue |
| 6 | índice da família onde é filho (`-1` se nenhuma) |
| 7 | índices das famílias onde é cônjuge |
| 8 | família (apelido) |
| 9 | referências cruzadas noutras genealogias |
| 10 | fontes (assentos onde aparece) |
| 11 | evidências opcionais dos originais: lista de objetos com `id`, `origem`, `url`, `imagem`, `lado`, `ordem` e `papel` |

Família `f[j]`: `[marido, mulher, data_casamento, nota, [filhos]]`, com `-1` para ausente.

### GEDCOM
5.5.1, UTF-8, `LINEAGE-LINKED`. Família e código do blogue vão em `NOTE`, não em etiquetas
próprias, para manter a compatibilidade com Gramps e MyHeritage.

---

## 5. Página

- Um só ficheiro `index.html`: `<title>`, `<meta>`, `<style>`, marcação e `<script>`.
- **Sem dependências externas** além das fontes do Google Fonts. Sem framework, sem bundler.
- JavaScript em ES5, sem módulos, dentro de uma IIFE. Sem estado global além de `window.ARVORE`.
- Os dados entram por `<script src="dados.js?v=N">`. **O `?v=N` sobe sempre que `dados.js`
  muda** — sem isso o GitHub Pages serve a versão antiga da cache.
- Construção do DOM por `document.createElement` e `textContent`. Não se usa `innerHTML` com
  dados: os nomes vêm de transcrições e podem conter qualquer coisa.
- Funções de apresentação: `fmt(data)` aplica a notação do DESIGN.md; `vida(i)` compõe
  `* nascimento † óbito`; `botaoPessoa(i)` é a única forma de mostrar uma pessoa clicável.

---

## 6. Publicação

Dois destinos, a partir dos mesmos ficheiros:

1. **GitHub Pages** — `index.html` + `dados.js` + `dados_s8.js` na raiz do repositório, ramo `main`.
   Público, com `<meta name="robots" content="noindex,nofollow">`.
   O build Jekyll usa `_config.yml` para excluir `fontes/` da publicação: as fotografias
   ficam no Git e são consultadas através das ligações ao arquivo; não são necessárias
   ao explorador. Evita-se enviar dezenas de GiB de fontes para o artefacto Pages.
2. **Artefacto privado** — a mesma página, com os mesmos dados, incluindo o suplemento S8.

A Drive guarda cópias de arquivo (GEDCOM, CSV, arquivo do blogue), não serve a página.

Depois de publicar confirma-se a versão em linha antes de dar por feito: a página tem de
responder com o `?v=N` novo e com os totais esperados.

---

## 7. Qualidade

Nenhuma correção de dados se faz à mão no resultado. O caminho é sempre: apertar uma regra
no parser ou na fusão, correr a cadeia, comparar totais e verificar na página publicada um
caso concreto conhecido.

Três relatórios acompanham cada geração e não devem desaparecer:
`duplicados.csv` (pares analisados e se foram fundidos), `suspeitas.csv` (ligações removidas
por serem impossíveis) e `conflitos_registos.csv` (divergências entre genealogia e assento).

`scripts/validar_design.py` confere `index.html` contra o `DESIGN.md`: cores literais fora dos
tokens, raios acima de 2px, sombras, tokens não definidos no bloco claro e notação das datas.
Corre-se antes de publicar.

A cadeia S8 verifica também datas dentro do intervalo do livro, IDs de assento únicos,
campos legíveis sem marcas de dúvida, índices recíprocos e separação de leituras pendentes.
