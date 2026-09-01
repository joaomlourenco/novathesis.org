---
title: Choosing which "list of…" gets printed
date: 2026-09-01
summary: One option turns off the List of Tables, Listings or Algorithms — without editing the configuration file that registers them.
image: toc.png
image_alt: A table of contents followed by a List of Figures
---

A thesis with two tables does not need a List of Tables. Until now, leaving one
out meant finding its line in `0-Config/6_list_of.tex` and commenting it out —
and remembering to put it back if a supervisor disagreed.

Since 8.3.0 there is an option for it:

```latex
\ntsetup{listof/skip={listoftables,listoflistings}}
```

That prints the List of Figures and nothing else. The lines in
`6_list_of.tex` stay exactly as they are.

## What you can name

Whatever `\ntaddlistof` registers — so the **full** list name, not a short
form:

* `listoffigures`
* `listoftables`
* `listofalgorithms`
* `listoflistings`
* any custom list you added yourself

And one extra, which is not a `\ntaddlistof` entry at all:

* `glossaries` — a friendlier spelling of `\ntsetup{print/glossaries=false}`

```latex
\ntsetup{listof/skip={listoftables,listofalgorithms,glossaries}}
```

The default is empty: nothing is skipped, and every list you registered is
printed.

## Why bother, when commenting out worked

Because the option lives with your other settings rather than inside the file
that declares the lists, and because it survives a template upgrade — you are
no longer maintaining a local edit to a shipped configuration file. It also
composes with `make`:

```bash
make NT="listof/skip={listoftables}"
```

which is handy when the same document has to be handed in twice, to two sets
of rules.
