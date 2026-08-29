#!/usr/bin/env python3
"""Render blog/*.md into en/blog/ and pt/blog/, plus Atom feeds.

    python3 tools/gen_blog.py

Posts live in blog/ as YYYY-MM-DD-slug.<lang>.md with front matter. See
blog/README.md for the authoring side. This script:

  * renders each post to <lang>/blog/<slug>.html
  * rebuilds <lang>/blog/index.html, the history, newest first
  * writes <lang>/blog/feed.xml (Atom)
  * keeps the Blog link in every page's nav

Page chrome (header, footer, <head> links) is lifted from <lang>/index.html
rather than duplicated here, so hand edits to the site's furniture reach the
blog automatically. Blog pages sit one directory deeper, so relative links are
rewritten as they are copied.

Idempotent: a second run reports "already up to date".
"""
import html, re, sys, glob, pathlib, datetime

SITE = pathlib.Path(__file__).resolve().parent.parent
BLOG = SITE / 'blog'
LANGS = ('en', 'pt')

# ── markdown: the stdlib has none. Prefer the module; fall back to Homebrew's
# libexec (brew install python-markdown ships a CLI, not an importable module);
# fall back again to the markdown_py CLI. ──────────────────────────────────────
def _markdown_renderer():
    try:
        import markdown
        return lambda t: markdown.markdown(t, extensions=['extra', 'sane_lists'])
    except ImportError:
        pass
    for p in glob.glob('/opt/homebrew/opt/python-markdown/libexec/lib/python*/site-packages') \
           + glob.glob('/usr/local/opt/python-markdown/libexec/lib/python*/site-packages'):
        sys.path.insert(0, p)
        try:
            import markdown
            return lambda t: markdown.markdown(t, extensions=['extra', 'sane_lists'])
        except ImportError:
            sys.path.pop(0)
    import shutil, subprocess
    cli = shutil.which('markdown_py')
    if cli:
        return lambda t: subprocess.run([cli, '-x', 'extra'], input=t, capture_output=True,
                                        text=True, check=True).stdout
    sys.exit("no Markdown renderer found — 'pip install markdown' or 'brew install python-markdown'")

render_md = _markdown_renderer()

STRINGS = {
 'en': dict(nav='Blog', title='Blog', lede='Release notes, new schools and notes from the project.',
            back='← All posts', empty='No posts yet.', only='Only available in English',
            other='Ler em português', readmore='Read'),
 'pt': dict(nav='Blog', title='Blog', lede='Notas de versão, novas escolas e notas do projecto.',
            back='← Todos os artigos', empty='Ainda não há artigos.', only='Só disponível em português',
            other='Read in English', readmore='Ler'),
}
MONTHS = {'en': 'January February March April May June July August September October November December'.split(),
          'pt': 'Janeiro Fevereiro Março Abril Maio Junho Julho Agosto Setembro Outubro Novembro Dezembro'.split()}

def fmt_date(d, lang):
    return f'{d.day} {MONTHS[lang][d.month-1]} {d.year}' if lang == 'en' \
      else f'{d.day} de {MONTHS[lang][d.month-1]} de {d.year}'

# ── parsing ───────────────────────────────────────────────────────────────────
NAME = re.compile(r'^(\d{4})-(\d{2})-(\d{2})-(?P<slug>[a-z0-9][a-z0-9-]*)\.(?P<lang>en|pt)\.md$')

def parse(path, problems):
    m = NAME.match(path.name)
    if not m:
        problems.append(f'{path.name}: name must be YYYY-MM-DD-slug.en.md (or .pt.md)'); return None
    text = path.read_text(encoding='utf-8')
    if not text.startswith('---'):
        problems.append(f'{path.name}: missing front matter'); return None
    _, fm, body = text.split('---', 2)
    meta = {}
    for line in fm.strip().split('\n'):
        if ':' in line:
            k, v = line.split(':', 1)
            meta[k.strip()] = v.split('#')[0].strip() if k.strip() in ('image', 'image_alt') else v.strip()
    if not meta.get('title'):
        problems.append(f'{path.name}: front matter needs a title'); return None
    fdate = datetime.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    if meta.get('date') and meta['date'] != fdate.isoformat():
        problems.append(f'{path.name}: front-matter date {meta["date"]} != filename date {fdate}')
    img = meta.get('image') or ''
    if img:
        if not (BLOG / 'images' / img).exists():
            problems.append(f'{path.name}: image {img} not found in blog/images/'); img = ''
        elif not meta.get('image_alt'):
            problems.append(f'{path.name}: image_alt is required when image is set'); img = ''
    return dict(slug=m.group('slug'), lang=m.group('lang'), date=fdate, title=meta['title'],
                summary=meta.get('summary', ''), image=img, image_alt=meta.get('image_alt', ''),
                body=render_md(body.strip()))

# ── page chrome, lifted from <lang>/index.html ────────────────────────────────
def chrome(lang):
    src = (SITE / lang / 'index.html').read_text(encoding='utf-8')
    head = ''.join(re.findall(r'<link rel="(?:preconnect|stylesheet|icon|me)"[^>]*>', src))
    header = re.search(r'<header class="hd">.*?</header>', src, re.S).group(0)
    footer = re.search(r'<footer class="ft">.*?</footer>', src, re.S).group(0)
    # the chrome comes from a page where Home is current; Blog is current here
    header = header.replace('class="on"', 'class=""')
    header = header.replace('href="blog/index.html">', 'href="blog/index.html" data-here>')
    header = header.replace('<a class="" href="blog/index.html" data-here>', '<a class="on" href="blog/index.html">')
    def deepen(s):                       # en/x.html -> en/blog/x.html: one level down
        s = s.replace('href="../', 'href="@@/')          # ../styles.css -> ../../
        s = re.sub(r'href="(?!https?:|#|@@/|\.\./)([^"]+)"', r'href="../\1"', s)
        return s.replace('href="@@/', 'href="../../')
    return head.replace('href="../', 'href="../../'), deepen(header), deepen(footer)

def page(lang, title, desc, body, extra_head=''):
    head, header, footer = CHROME[lang]
    return (f'<!DOCTYPE html>\n<html lang="{lang}">\n<head>\n<meta charset="utf-8">\n'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            f'<title>{html.escape(title)} · novathesis</title>\n'
            f'<meta name="description" content="{html.escape(desc)}">\n{head}\n{extra_head}</head>\n'
            f'<body>\n<div class="wrap">\n{header}\n<main class="page">\n{body}\n</main>\n{footer}\n</div>\n'
            f'</body>\n</html>\n')

def og(lang, title, desc, url, image):
    tags = [f'<meta property="og:type" content="article">',
            f'<meta property="og:title" content="{html.escape(title)}">',
            f'<meta property="og:description" content="{html.escape(desc)}">',
            f'<meta property="og:url" content="{url}">',
            f'<meta property="og:site_name" content="novathesis">',
            f'<meta property="og:locale" content="{"en_GB" if lang=="en" else "pt_PT"}">']
    if image:
        tags += [f'<meta property="og:image" content="https://novathesis.org/blog/images/{image}">',
                 '<meta name="twitter:card" content="summary_large_image">']
    else:
        tags.append('<meta name="twitter:card" content="summary">')
    return '\n'.join(tags) + '\n'

# ── rendering ─────────────────────────────────────────────────────────────────
def post_page(p, others, lang):
    s, url = STRINGS[lang], f'https://novathesis.org/{lang}/blog/{p["slug"]}'
    hero = (f'<figure class="post-hero"><img src="../../blog/images/{p["image"]}" '
            f'alt="{html.escape(p["image_alt"])}"></figure>\n') if p['image'] else ''
    swap = ''
    if others:
        o = 'pt' if lang == 'en' else 'en'
        swap = f' · <a href="../../{o}/blog/{p["slug"]}.html">{STRINGS[lang]["other"]}</a>'
    body = (f'<div class="lede post-head"><div class="kicker">{fmt_date(p["date"], lang)}{swap}</div>'
            f'<h1>{html.escape(p["title"])}</h1>'
            + (f'<p>{html.escape(p["summary"])}</p>' if p['summary'] else '') + '</div>\n'
            + hero + f'<article class="post">\n{p["body"]}\n</article>\n'
            f'<p class="post-back"><a href="index.html">{s["back"]}</a></p>')
    return page(lang, p['title'], p['summary'] or p['title'], body,
                og(lang, p['title'], p['summary'] or p['title'], url, p['image']))

def index_page(posts, lang):
    s = STRINGS[lang]
    items = []
    for p in posts:
        thumb = (f'<a class="post-thumb" href="{p["slug"]}.html"><img src="../../blog/images/{p["image"]}" '
                 f'alt="{html.escape(p["image_alt"])}" loading="lazy"></a>') if p['image'] else ''
        only = '' if p['both'] else f' <span class="tag">{s["only"]}</span>'
        items.append(f'<article class="post-item{"" if p["image"] else " no-thumb"}">{thumb}<div class="post-meta">'
                     f'<div class="kicker">{fmt_date(p["date"], lang)}{only}</div>'
                     f'<h2><a href="{p["slug"]}.html">{html.escape(p["title"])}</a></h2>'
                     + (f'<p>{html.escape(p["summary"])}</p>' if p['summary'] else '')
                     + f'<a class="more" href="{p["slug"]}.html">{s["readmore"]} →</a></div></article>')
    body = (f'<div class="lede"><h1>{s["title"]}</h1><p>{s["lede"]}</p></div>\n'
            f'<div class="post-list">\n' + ('\n'.join(items) if items else f'<p>{s["empty"]}</p>') + '\n</div>')
    return page(lang, s['title'], s['lede'], body,
                f'<link rel="alternate" type="application/atom+xml" title="novathesis blog" href="feed.xml">\n')

def feed(posts, lang):
    updated = max((p['date'] for p in posts), default=datetime.date.today())
    e = []
    for p in posts:
        url = f'https://novathesis.org/{lang}/blog/{p["slug"]}'
        e.append(f'  <entry>\n    <title>{html.escape(p["title"])}</title>\n'
                 f'    <link href="{url}"/>\n    <id>{url}</id>\n'
                 f'    <updated>{p["date"].isoformat()}T00:00:00Z</updated>\n'
                 f'    <summary>{html.escape(p["summary"] or p["title"])}</summary>\n  </entry>')
    return ('<?xml version="1.0" encoding="utf-8"?>\n<feed xmlns="http://www.w3.org/2005/Atom">\n'
            f'  <title>novathesis — {STRINGS[lang]["title"]}</title>\n'
            f'  <link href="https://novathesis.org/{lang}/blog/"/>\n'
            f'  <link rel="self" href="https://novathesis.org/{lang}/blog/feed.xml"/>\n'
            f'  <id>https://novathesis.org/{lang}/blog/</id>\n'
            f'  <updated>{updated.isoformat()}T00:00:00Z</updated>\n' + '\n'.join(e) + '\n</feed>\n')

# ── nav: add Blog to every page, once, after Showcase ─────────────────────────
def sync_nav():
    changed = []
    for lang in LANGS:
        label = STRINGS[lang]['nav']
        for f in sorted((SITE / lang).glob('*.html')):
            s = f.read_text(encoding='utf-8')
            if f'>{label}</a>' in s:
                continue
            show = re.search(r'<a class="[^"]*" href="showcase\.html">[^<]*</a>', s)
            if not show:
                continue
            s2 = s[:show.end()] + f'<a class="" href="blog/index.html">{label}</a>' + s[show.end():]
            f.write_text(s2, encoding='utf-8'); changed.append(f'{lang}/{f.name}')
    return changed

def write(path, text, written):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.read_text(encoding='utf-8') == text:
        return
    path.write_text(text, encoding='utf-8'); written.append(str(path.relative_to(SITE)))

CHROME = {}
def main():
    problems, written, removed = [], [], []
    parsed = [q for q in (parse(p, problems) for p in sorted(BLOG.glob('*.md'))
                          if not p.name.startswith('_') and p.name != 'README.md') if q]
    slugs = {}
    for p in parsed:
        slugs.setdefault(p['slug'], {})[p['lang']] = p
    nav = sync_nav()                 # before chrome(): it edits the pages chrome is lifted from
    for lang in LANGS:
        CHROME[lang] = chrome(lang)
    for lang in LANGS:
        posts = sorted((dict(v[lang], both=len(v) == 2) for v in slugs.values() if lang in v),
                       key=lambda p: (p['date'], p['slug']), reverse=True)
        for p in posts:
            write(SITE / lang / 'blog' / f'{p["slug"]}.html',
                  post_page(p, p['both'], lang), written)
        write(SITE / lang / 'blog' / 'index.html', index_page(posts, lang), written)
        write(SITE / lang / 'blog' / 'feed.xml', feed(posts, lang), written)
        # a renamed or deleted post must not leave its page published
        keep = {f'{p["slug"]}.html' for p in posts} | {'index.html'}
        for stale in sorted((SITE / lang / 'blog').glob('*.html')):
            if stale.name not in keep:
                stale.unlink(); removed.append(str(stale.relative_to(SITE)))
        print(f'  {lang}: {len(posts)} post(s)')
    if nav:
        print(f'  nav: Blog link added to {len(nav)} page(s)')
    print('\n' + (f'wrote {len(written)} file(s):' if written else 'already up to date'))
    for w in written:
        print('  ·', w)
    if removed:
        print(f'removed {len(removed)} stale page(s):')
        for r in removed:
            print('  ·', r)
    if problems:
        print('\nproblems:')
        for p in problems:
            print('  ·', p)
        sys.exit(1)

main()
