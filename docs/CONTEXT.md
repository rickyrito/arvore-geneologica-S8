# CONTEXT.md — Árvore Genealógica, Família Rito do Soito

Regras de negócio. Valem acima de qualquer conveniência técnica: um ecrã mais bonito ou um
número maior de pessoas não justifica quebrar nenhuma delas.

---

## 1. O que é

Uma base genealógica da freguesia do **Soito (Sabugal, antiga Riba-Côa, bispado de Pinhel)**,
construída por leitura automática dos 294 artigos do blogue **Saber Soito**, de **Carlos**
(`ticarlos@sapo.pt`), e apresentada numa página de consulta.

Não é um produto, não tem contas de utilizador nem autenticação. Tem dois usos:

1. **Consulta pela família** — procurar uma pessoa e andar para cima e para baixo na árvore.
2. **Revisão pelo autor da investigação** — ver onde as fontes dele se contradizem.

---

## 2. Quem usa

- **Ricardo Rito** — mantém a base; entra pelos seus próprios antepassados e confere
  pessoas que conhece de cor. Foram esses testes que apanharam os erros mais graves.
- **Carlos, autor do blogue** — não trabalha com ficheiros técnicos. Recebe um `.xlsx`
  legível com as divergências entre as transcrições dele, e o endereço da página.
- **Familiares** — abrem o endereço no telemóvel, sem conta nenhuma e sem instalar nada.

---

## 3. Proveniência (nunca violar)

1. **Todos os dados vêm do blogue.** Não se acrescenta informação de outra fonte sem a
   marcar visivelmente como tal.
2. **A atribuição ao Carlos não se remove** — está no rodapé da página e no README, e
   mantém-se em qualquer versão nova.
3. **Cada pessoa mostra as suas fontes** na secção «Assentos»: o assento e o artigo de onde
   veio. Pessoa sem fonte identificada di-lo expressamente.
4. **Nada se corrige à mão no resultado.** Corrige-se a regra e volta a gerar-se tudo.

---

## 4. Regras genealógicas de ligação

Aplicadas na fusão e verificadas de novo no fim da cadeia:

1. **Irmãos nunca são a mesma pessoa.** Duas pessoas filhas da mesma família não se fundem,
   mesmo com nome idêntico — repetir o nome de um filho falecido era prática corrente
   (há 1254 casos na base).
2. **Nome próprio tem de coincidir.** Partilhar os apelidos finais não basta para tratar duas
   pessoas como a mesma.
3. **Códigos distintos dentro da mesma família são pessoas distintas.** Entre famílias
   diferentes, o mesmo código pode ser a mesma pessoa e a fusão é registada como referência
   cruzada.
4. **Datas incompatíveis bloqueiam a fusão:** se uma morreu antes de a outra nascer, são
   pessoas diferentes.
5. **Ninguém casa depois de morto**, nem antes dos 12 anos.
6. **Progenitor entre 12 e 70 anos mais velho que o filho**, e vivo à data do nascimento.
7. **Filho liga ao casamento compatível com a sua data de nascimento**, não ao primeiro
   casamento do progenitor.

---

## 5. Conflitos e remoções

1. **Em divergência entre a genealogia de família e o assento, vale a genealogia** — e a
   divergência fica registada em `conflitos_registos.csv`. Nunca se escolhe em silêncio.
2. **Tudo o que é removido fica num relatório.** Ligação desfeita por ser impossível vai para
   `suspeitas.csv` com o motivo; pares avaliados para fusão vão para `duplicados.csv`, com a
   indicação de terem sido ou não fundidos.
3. **Incerteza mostra-se, não se esconde.** Pessoa sem data mostra `—`; progenitor sem
   registo aparece como `desconhecido`; nunca se inventa uma data aproximada que a fonte não dê.

---

## 6. Pessoas vivas

A página pública mostra nomes e datas completos, incluindo de pessoas vivas, por decisão
expressa do Ricardo e porque o blogue de origem já os publica. Em contrapartida:

- a página leva `noindex, nofollow`, para não ser indexada por motores de busca;
- existe no histórico do projeto uma variante com as pessoas possivelmente vivas ocultadas
  («pessoa viva», sem datas), para o caso de ser preciso voltar a ela;
- a decisão de divulgar o endereço é sempre do Ricardo.

---

## 7. Apresentação

- A notação das datas é a genealógica corrente: `*` nascimento, `~` batismo, `†` óbito,
  `⚭` casamento, em `DD-MM-AAAA` (ver DESIGN.md).
- Os códigos do blogue (`2:1:6:6:11`) são mostrados tal como lá estão: são a chave para
  voltar à fonte.
- A página abre numa pessoa concreta e útil, nunca vazia.
- Funciona no telemóvel sem scroll horizontal.
