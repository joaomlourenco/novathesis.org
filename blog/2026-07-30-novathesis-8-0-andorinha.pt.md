---
title: novathesis 8.0.0 — Swallow: Migration Season
date: 2026-07-30
summary: Os glossários passam para o bib2gls — uma migração que todos os documentos existentes têm de fazer — e as compilações em pdfLaTeX ficam cerca de três vezes mais rápidas.
image: flying-swallow.png
image_alt: Uma andorinha em voo
---

A Andorinha é a versão em que os glossários mudaram de motor. Torna as
compilações muito mais rápidas, mas pede-te uma coisa primeiro.

## Alteração incompatível: os glossários passam a usar o `bib2gls`

Os acrónimos, os termos de glossário e os símbolos passam a ser definidos em
ficheiros **`.bib`** processados pelo `bib2gls`, em vez de ficheiros `.tex`
processados pelo `makeglossaries`. Os documentos existentes têm de ser
migrados:

```bash
make glsbib     # converte os ficheiros 1-FrontMatter/*.tex para .bib
```

Depois, antes de apagares os ficheiros antigos:

* **Volta a pôr as chaves `sort`.** O `convertgls2bib` descarta-as em silêncio
  e, sem elas, os símbolos saem pela ordem errada. O `make glsbib` conta-as e
  avisa-te ficheiro a ficheiro.
* Muda as entradas de símbolos de `@entry` para `@symbol`.
* Apaga o `\glsaddall` se o usares — o `bib2gls` não tem equivalente.

Não é possível falhar a migração por distracção: um ficheiro `.tex` de entradas
que fique para trás **interrompe a compilação**, com um erro que indica a causa
e a solução. O procedimento completo está no apêndice *Migrating from 7.10.x*
do manual.

**Um novo requisito:** o `bib2gls` precisa de um ambiente de execução Java. Vem
com o TeX Live e o Overleaf tem um; localmente, confirma com
`bib2gls --version`.

## Em troca: compilações muito mais rápidas

Os glossários deixam de consumir os 16 registos de escrita do pdfTeX, por isso
o pacote `morewrites` — que tornava cada passagem cerca de nove vezes mais
lenta — deixa de ser carregado por omissão. Uma compilação completa do manual
em pdfLaTeX passou de **109 segundos para 36**. Os glossários também deixam de
precisar de `-shell-escape`.

## Também é novo

**Opções na linha de comandos.** Define qualquer opção do `\ntsetup` no momento
da compilação, sem mexer em ficheiros de configuração:

```bash
make NT="doctype=msc,lang=pt"
```

**Um sistema de compilação reconstruído.** O `Makefile` passa a ser uma camada
fina sobre o `latexmk`, com as definições de LaTeX no `latexmkrc`. O manual tem
um novo apêndice *Build System*.

Vieram várias correcções, entre elas os marcadores de PDF para entradas
`\ntindex` sem parênteses rectos e as capas com nomes empilhados usadas pela
UMinho e pelo ISEL-MEB. A lista completa está no
[changelog](https://github.com/joaomlourenco/novathesis/blob/main/CHANGELOG.md).
