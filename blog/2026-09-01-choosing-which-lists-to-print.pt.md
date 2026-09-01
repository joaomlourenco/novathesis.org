---
title: Escolher que "lista de…" é impressa
date: 2026-09-01
summary: Uma opção desliga a Lista de Tabelas, de Listagens ou de Algoritmos — sem editar o ficheiro de configuração que as registou.
image: toc.png
image_alt: Um índice seguido de uma Lista de Figuras
---

Uma tese com duas tabelas não precisa de uma Lista de Tabelas. Até agora, deixar
uma de fora obrigava a procurar a linha respectiva em
`0-Config/6_list_of.tex`, comentá-la — e lembrar-se de a repor se o orientador
discordasse.

Desde a versão 8.3.0 há uma opção para isso:

```latex
\ntsetup{listof/skip={listoftables,listoflistings}}
```

Isto imprime a Lista de Figuras e mais nada. As linhas do `6_list_of.tex`
ficam exactamente como estão.

## O que podes indicar

Aquilo que o `\ntaddlistof` registou — ou seja, o nome **completo** da lista, e
não uma forma abreviada:

* `listoffigures`
* `listoftables`
* `listofalgorithms`
* `listoflistings`
* qualquer lista personalizada que tenhas acrescentado

E um extra, que não é sequer uma entrada do `\ntaddlistof`:

* `glossaries` — forma mais simpática de escrever `\ntsetup{print/glossaries=false}`

```latex
\ntsetup{listof/skip={listoftables,listofalgorithms,glossaries}}
```

Por omissão está vazio: nada é saltado e todas as listas registadas são
impressas.

## Porquê, se comentar a linha funcionava

Porque a opção fica junto das tuas outras configurações, em vez de dentro do
ficheiro que declara as listas, e porque sobrevive a uma actualização do
template — deixas de manter uma alteração local a um ficheiro de configuração
que vem com o template. Também se combina com o `make`:

```bash
make NT="listof/skip={listoftables}"
```

o que é prático quando o mesmo documento tem de ser entregue duas vezes, com
dois conjuntos de regras.
