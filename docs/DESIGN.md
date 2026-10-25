# DESIGN.md — Árvore Genealógica, Família Rito do Soito

Regras de desenho da página `index.html`. Documentam o que está implementado; qualquer
componente novo segue isto à letra, sem introduzir valores fora desta lista.

Princípio: a página é um instrumento de consulta de registos paroquiais. O desenho é sóbrio,
de papel e tinta, com uma única cor de acento. Nada de sombras, gradientes ou cantos
arredondados grandes.

---

## 1. Cores

Todas as cores são tokens em `:root`. **Nenhum componente usa valores literais.**

| Token | Claro | Escuro | Uso |
|---|---|---|---|
| `--papel` | `#f4f4f0` | `#14171b` | fundo da página; fundo da coluna de pesquisa fixa |
| `--papel-2` | `#eceae3` | `#1b1f25` | fundo de qualquer superfície elevada: cartão, campo de formulário, botão de pessoa, nó da ascendência |
| `--tinta` | `#1f2328` | `#e8e6e0` | texto corrente, títulos, filete inferior do cabeçalho |
| `--tinta-fraca` | `#5d6670` | `#9aa3ad` | texto secundário: datas, rótulos, legendas, notas dos assentos |
| `--linha` | `#d8d5cb` | `#2c323a` | **todas as bordas e separadores**, salvo as exceções da secção 2 |
| `--azulejo` | `#2d4f7c` | `#8fb3dd` | acento: ligações, foco, filete das datas, borda da etiqueta de referência cruzada |
| `--azulejo-claro` | `#e3ebf5` | `#1e2832` | fundo de realce: linha da lista sob o cursor, etiqueta de referência cruzada |
| `--ocre` | `#8a6a2f` | `#d2ab63` | códigos do blogue e datas de casamento — e nada mais |

Os três blocos de tema são obrigatórios e redefinem **apenas tokens**:

```css
:root { /* valores claros, todos os tokens */ }
@media (prefers-color-scheme:dark){ :root:not([data-theme="light"]) { /* valores escuros */ color-scheme:dark } }
:root[data-theme="dark"]{ /* os mesmos valores escuros */ color-scheme:dark }
```

`body` declara sempre `background:var(--papel)`; fundo transparente deixa passar o tema do
anfitrião e parte a leitura.

### Semântica da cor

- **Ocre** marca proveniência: código do blogue (`2:1:6:6:11`) e data de casamento (`⚭ 27-08-1978`).
- **Azulejo** marca navegação e ligação entre fontes: links, foco, referências cruzadas.
- Não há cores de estado (sucesso, erro, aviso). Dados ausentes escrevem-se `—` em `--tinta-fraca`.

---

## 2. Bordas

Regra geral: **1px sólido `var(--linha)`, raio 2px.** O raio nunca passa de 2px.

| Elemento | Borda |
|---|---|
| Cartão da ficha (`.cartao`) | `1px solid var(--linha)`, raio 2px |
| Campo de texto e selecção (`.busca input`, `.busca select`) | `1px solid var(--linha)`, raio 2px |
| Etiqueta (`.chip`) | `1px solid var(--linha)`, raio 2px |
| Etiqueta de código (`.chip.cod`) | `1px solid var(--ocre)` |
| Etiqueta de referência cruzada (`.chip.ref`) | `1px solid var(--azulejo)` + fundo `--azulejo-claro` |
| Botão de pessoa (`.pbtn`) e nó da ascendência (`.no`) | `1px solid var(--linha)`, raio 2px; ao passar o cursor a borda muda para `--azulejo` |
| Linha da lista (`.lista li`) | só `border-bottom:1px solid var(--linha)` |
| Título de secção (`h3`) | só `border-bottom:1px solid var(--linha)` |
| Rodapé | só `border-top:1px solid var(--linha)` |

Três exceções deliberadas, todas filetes de 2px à esquerda ou em baixo, que marcam hierarquia
e não contorno:

- Cabeçalho da página: `border-bottom:2px solid var(--tinta)`
- Campo de data na ficha (`.datas div`): `border-left:2px solid var(--azulejo)`
- Bloco de casamento (`.casamento`): `border-left:3px solid var(--ocre)`
- Linha de assento (`.fontes li`): `border-left:2px solid var(--linha)`

**Proibido**: `box-shadow`, `outline` decorativo, bordas duplas, bordas a mais do que uma cor
no mesmo elemento, raios acima de 2px.

Foco de teclado: `outline:2px solid var(--azulejo); outline-offset:1px`. Nunca se remove sem
substituir por marca visível equivalente.

---

## 3. Tipografia

| Token | Família | Uso |
|---|---|---|
| `--display` | `"Faustina", Georgia, "Times New Roman", serif` | `h1`, `h2` — nome da pessoa e título da página |
| `--corpo` | `"IBM Plex Sans", system-ui, -apple-system, "Segoe UI", sans-serif` | tudo o resto, incluindo `h3` |

- Títulos de secção (`h3`): 13px, maiúsculas, `letter-spacing:.1em`, peso 600, cor `--tinta-fraca`.
- Rótulos pequenos (`.contagem`, `.datas dt`, `.col .rot`): 11–12px, maiúsculas, `letter-spacing` entre `.04em` e `.08em`, cor `--tinta-fraca`.
- Qualquer elemento que mostre datas ou números em coluna leva `font-variant-numeric:tabular-nums`.
- Nome da pessoa no cartão: `clamp(21px,3vw,27px)`, peso 600.

---

## 4. Espaçamento e layout

- Espaçamentos entre irmãos fazem-se com `gap` em flex ou grid, nunca com margens soltas.
- Escala usada: 2, 6, 8, 10, 12, 18, 20, 22, 28 px.
- Goteira lateral da página: `padding-left/right: max(16px, env(safe-area-inset-*, 0px))`.
- Grelha principal: `minmax(260px,330px)` para a pesquisa e `minmax(0,1fr)` para a ficha;
  abaixo de 820px passa a uma coluna.
- A coluna de pesquisa é `position:sticky` no topo em ecrã largo e estática no telemóvel.
- Nenhum elemento tem `min-width` superior à largura do ecrã; blocos com texto longo levam
  `min-width:0` e `overflow-wrap:anywhere`.

---

## 5. Notação genealógica

Obrigatória em qualquer sítio onde apareçam datas de pessoas:

| Símbolo | Significado | Exemplo |
|---|---|---|
| `*` | nascimento | `* 12-05-1940` |
| `~` | batismo | `~ 27-04-1952` |
| `†` | óbito | `† 15-08-2020` |
| `⚭` | casamento | `⚭ 26-08-1939` |

Datas em `DD-MM-AAAA`, com hífen. Quem não tem data de nascimento conhecida mostra só o óbito,
sem inventar aproximações. Datas aproximadas da fonte escrevem-se `c. 1855`.

---

## 6. Componente: cartão de pessoa

Composição, de cima para baixo:

1. **Nome** — `h2`, `--display`, peso 600.
2. **Etiquetas** (`.chips`) — família, código do blogue (ocre), referências cruzadas (azulejo), sexo. Ordem fixa.
3. **Datas** (`.datas`) — grelha `repeat(auto-fit,minmax(130px,1fr))`, cada campo com filete azulejo à esquerda, rótulo em maiúsculas com o símbolo (`* Nascimento`, `~ Batismo`, `† Óbito`) e valor em 17px tabular.
4. **Secções seguintes** — Ascendência, Casamentos e filhos, Irmãos, Assentos; cada uma com `h3` sublinhado e o conteúdo em botões de pessoa.

Regras do cartão:

- Fundo `--papel-2`, borda `1px solid var(--linha)`, `padding:20px`, sem sombra.
- Campo sem valor mostra `—` em `--tinta-fraca`; nunca se esconde o campo.
- Toda a pessoa referida é um botão clicável que leva à ficha dela; pessoas sem registo próprio
  aparecem como texto em itálico `desconhecido`, em `--tinta-fraca`, sem borda de realce.
- Notas dos assentos aparecem em `--tinta-fraca`, 13.5px, largura máxima 68 caracteres.

---

## 7. Proveniência

Tudo o que a página mostra vem do blogue [Saber Soito](https://soitoribacoa.blogspot.com/),
de Carlos. O rodapé diz isso em todas as versões e a atribuição não se remove. Dados
acrescentados por outra via têm de ser visivelmente distinguidos da transcrição original.
