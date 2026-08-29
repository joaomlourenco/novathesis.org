---
title: novathesis 8.0 — Andorinha
date: 2026-07-30
summary: Glossaries move to bib2gls — a migration every existing document needs — and pdfLaTeX builds get about three times faster.
image:
image_alt:
---

Andorinha is the release where glossaries changed engine. It makes builds much
faster, and it asks something of you first.

## Breaking: glossaries now use `bib2gls`

Acronyms, glossary terms and symbols are defined in **`.bib` files** processed
by `bib2gls`, instead of `.tex` files processed by `makeglossaries`. Existing
documents must be migrated:

```bash
make glsbib     # converts 1-FrontMatter/*.tex entry files to .bib
```

Then, before you delete the old files:

* **Re-add any `sort` keys.** `convertgls2bib` drops them silently, and without
  them symbols come out in the wrong order. `make glsbib` counts them and warns
  you per file.
* Change symbol entries from `@entry` to `@symbol`.
* Delete `\glsaddall` if you call it — `bib2gls` has no equivalent.

You cannot miss the migration by accident: a leftover `.tex` entry file now
**stops the build** with an error naming the cause and the fix. The full
procedure is the *Migrating from 7.10.x* appendix of the manual.

**One new requirement:** `bib2gls` needs a Java runtime. It ships with TeX Live
and Overleaf provides one; check locally with `bib2gls --version`.

## In exchange: much faster builds

Glossaries no longer consume any of pdfTeX's 16 write registers, so the
`morewrites` package — which made every pass about nine times slower — is no
longer loaded by default. A full pdfLaTeX build of the manual went from **109
seconds to 36**. Glossaries no longer need `-shell-escape` either.

## Also new

**Command-line overrides.** Set any `\ntsetup` option at build time, without
touching a configuration file:

```bash
make NT="doctype=msc,lang=pt"
```

**A rebuilt build system.** The `Makefile` is now a thin wrapper over
`latexmk`, with all LaTeX settings in `latexmkrc`. There is a new *Build
System* appendix in the manual.

Several fixes came with it, including PDF bookmarks for bracketless
`\ntindex` entries and the stacked-name covers used by UMinho and ISEL-MEB.
The full list is in the
[changelog](https://github.com/joaomlourenco/novathesis/blob/main/CHANGELOG.md).
