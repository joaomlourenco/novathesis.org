# novathesis.org

Source of the **novathesis.org** website — the public site for the
[NOVAthesis](https://github.com/joaomlourenco/novathesis) LaTeX template for
theses and dissertations.

Static HTML and CSS. No build step, no dependencies, no framework: the pages
are served exactly as they are committed. The one exception is the showcase
gallery, which is generated (see [Regenerating the showcase](#regenerating-the-showcase)).

## Layout

```
index.html          language redirect
styles.css          the entire stylesheet, shared by every page
en/ , pt/           one folder per language, same 7 pages in each
covers/SVG/         cover, front-page, chapter and spine samples
tools/              gen_showcase.py
```

Pages: `index`, `schools`, `start`, `docs`, `showcase`, `support`, `contributing`.

## Both languages, always

Every page exists twice, `en/` and `pt/`, and the two are kept **equivalent**:
any change to one is made to the other in the same commit. The header carries a
`EN`/`PT` switch that links to the same page in the other language, so the file
names must stay in step.

## Cover assets

Files in `covers/SVG/` follow one naming convention:

```
<school>[-<variant>]-<degree>-<lang>-<engine>-<page>.svg
   nova-fct           -phd -en -lua -1.svg
   nova-itqb -green   -phd -en -lua -S.svg
```

`<page>` is what the file shows:

| code | page |
|------|------|
| `N`  | back cover |
| `1`  | front cover |
| `2`  | front page |
| `L1` | first page of an example chapter |
| `S`  | spine |

Not every school has every page — missing ones are simply omitted from the
gallery. Two details worth knowing before editing the CSS:

* **Spines are exported horizontally** (297 mm × 10 mm, so a wide, thin strip)
  and are **transparent outside the artwork**. That is why the spine has no
  frame or white background in the showcase: a frame would show as white
  margins at both ends. `nova-fct-cbbi` is a thicker 30 mm spine, so any
  fixed-pixel cropping would break it.
* **`uminho` covers are wrap-arounds** (back + spine + front in one image), so
  they are roughly twice as wide as an A4 page. The showcase detects any image
  wider than it is tall and gives it a double-width slot.

## Regenerating the showcase

`en/showcase.html` and `pt/showcase.html` are **generated** — do not hand-edit
the `<main>` element, it will be overwritten. After adding or replacing files in
`covers/SVG/`:

```bash
python3 tools/gen_showcase.py
```

It rewrites `<main>` in both languages, leaves the rest of each page untouched,
and reports any block missing a spine. Institution names and the block order
live in the tables at the top of the script; the English and Portuguese names
were taken from the template's own `\SetUniversity` / `\SetSchool` strings, so
keep them in step with the template rather than translating by hand.

## Conventions

* **The brand is written `<b>nova</b>thesis` in body copy** — never in headings,
  `<title>`, `meta` descriptions or `alt` text, where the markup either does not
  render or would render backwards (headings are weight 800, `<b>` is 700).
  A CSS rule neutralises `<b>` inside headings, chips and buttons as a safety net.
* **Never wrap the name in URLs.** `github.com/novathesis/…`, `novathesisFiles`
  and `1_novathesis.tex` are identifiers, not the brand.
* **Overleaf links** use the import API so they always open the current version
  rather than the outdated official Overleaf template:
  `https://www.overleaf.com/docs?snip_uri=<repo>/archive/refs/heads/main.zip&main_document=template.tex`

## Local preview

```bash
python3 -m http.server 8000
```

Then open <http://localhost:8000/en/>. A plain file server is enough; opening
the files over `file://` also works, but a server matches how the site is
actually served.

## Licence

The NOVAthesis template is released under the
[LaTeX Project Public License 1.3c](https://www.latex-project.org/lppl/lppl-1-3c).
This repository holds the website source and carries no separate licence file yet.
