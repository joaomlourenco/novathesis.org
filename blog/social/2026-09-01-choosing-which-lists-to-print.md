# Social copy — "Choosing which list of… gets printed"

Post: https://novathesis.org/en/blog/choosing-which-lists-to-print
       https://novathesis.org/pt/blog/choosing-which-lists-to-print
Image: blog/images/toc.png

---

## Bluesky — EN (limit 300)

A thesis with two tables does not need a List of Tables.

Since novathesis 8.3.0 one option leaves it out, with no edit to the file that declares your lists:

\ntsetup{listof/skip={listoftables,listoflistings}}

https://novathesis.org/en/blog/choosing-which-lists-to-print

## Bluesky — PT (limite 300)

Uma tese com duas tabelas não precisa de Lista de Tabelas.

Desde o novathesis 8.3.0 há uma opção que a deixa de fora, sem tocar no ficheiro que declara as listas:

\ntsetup{listof/skip={listoftables,listoflistings}}

https://novathesis.org/pt/blog/choosing-which-lists-to-print

---

## Mastodon — EN (limit 500)

A thesis with two tables does not need a List of Tables.

Since novathesis 8.3.0, one option leaves any list out — and the lines in 0-Config/6_list_of.tex stay exactly as they are, so the setting survives a template upgrade:

\ntsetup{listof/skip={listoftables,listoflistings}}

Name the full list — listoftables, not tables. #LaTeX #PhD #thesis

https://novathesis.org/en/blog/choosing-which-lists-to-print

## Mastodon — PT (limite 500)

Uma tese com duas tabelas não precisa de Lista de Tabelas.

Desde o novathesis 8.3.0, uma opção deixa de fora qualquer lista — e as linhas do 0-Config/6_list_of.tex ficam como estão, pelo que a definição sobrevive a uma actualização do template:

\ntsetup{listof/skip={listoftables,listoflistings}}

Indica o nome completo: listoftables, não tables. #LaTeX #tese

https://novathesis.org/pt/blog/choosing-which-lists-to-print

---

## X — EN (limit 280)

A thesis with two tables does not need a List of Tables.

novathesis 8.3.0 leaves it out with one option, no edit to the file that declares your lists:

\ntsetup{listof/skip={listoftables,listoflistings}}

https://novathesis.org/en/blog/choosing-which-lists-to-print

## X — PT (limite 280)

Uma tese com duas tabelas não precisa de Lista de Tabelas.

O novathesis 8.3.0 deixa-a de fora com uma opção, sem tocar no ficheiro que declara as listas:

\ntsetup{listof/skip={listoftables,listoflistings}}

https://novathesis.org/pt/blog/choosing-which-lists-to-print

---

## Instagram — caption (image: toc.png; no clickable links, so link in bio)

A thesis with two tables does not need a List of Tables. 📑

Since novathesis 8.3.0 one line of configuration decides which "list of…" gets printed and which ones are skipped — the List of Tables, of Listings, of Algorithms, or the glossaries — without editing the file that declares them. Change your mind before the deadline and it is one word, not a hunt through a configuration file.

Full how-to on the blog, link in bio. 🔗

PT: Uma tese com duas tabelas não precisa de Lista de Tabelas. Desde o novathesis 8.3.0, uma linha decide que listas são impressas e que listas ficam de fora. Artigo completo no blogue, link na bio.

#LaTeX #novathesis #tese #thesis #PhD #MSc #dissertação #academia #phdlife
#writingatthesis #overleaf

---

## Reddit — r/LaTeX (title + body)

**Title:** novathesis 8.3.0: choosing which "list of…" gets printed, without editing the file that declares them

**Body:**

Small quality-of-life feature in the novathesis thesis template that may be of interest beyond it, since the pattern is reusable.

The template registers each front-matter list with \ntaddlistof. Leaving one out used to mean commenting out its line in the shipped configuration file — a local edit you then carry across every upgrade, and revert if a supervisor disagrees.

Since 8.3.0 there is an option instead:

    \ntsetup{listof/skip={listoftables,listoflistings}}

Values are the full registered names — listoffigures, listoftables, listofalgorithms, listoflistings, plus any list you added yourself. The odd one out is `glossaries`, which is a friendlier spelling of print/glossaries=false.

It also composes with the makefile, which is handy when the same document has to be submitted twice, to two sets of rules:

    make NT="listof/skip={listoftables}"

Write-up: https://novathesis.org/en/blog/choosing-which-lists-to-print Template: https://github.com/joaomlourenco/novathesis