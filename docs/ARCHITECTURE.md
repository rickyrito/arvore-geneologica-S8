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
                      duplicados, suspeitas, conflitos_registos
```

Regra: tudo em `/dados` e `dados.js` é **gerado**. Corrige-se o parser e volta-se a gerar;
não se edita o resultado.

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
| 12 | `ged_final.py` | 11 | `familia_soito.ged`, `dados.js` |

Correr a cadeia inteira é a forma normal de aplicar qualquer correção; não há atalhos por
etapas isoladas, porque as fusões dependem do que veio antes.

---

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

1. **GitHub Pages** — `index.html` + `dados.js` na raiz do repositório, ramo `main`.
   Público, com `<meta name="robots" content="noindex,nofollow">`.
2. **Artefacto privado** — a mesma página, com os mesmos dados.

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
