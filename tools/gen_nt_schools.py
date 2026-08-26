#!/usr/bin/env python3
"""Regenerate tools/nt_schools.py from schools.conf + .clo files + nt_overrides.py.

    python3 tools/gen_nt_schools.py

Bilingual university/school display names, and which doctypes actually have
cover art, are derived from the sibling novathesis LaTeX repo's
.Build/schools.conf and novathesisFiles/Schools/**/*.clo files, gated by what
actually exists in covers/SVG/. Everything with no source of truth there --
tag, credit, GROUPS, REPOS, custom per-degree block labels, which
schools.conf paths merge into one showcase row -- comes from nt_overrides.py
and passes through unchanged. Edit nt_overrides.py, not nt_schools.py.

The novathesis repo checkout is located via the NOVATHESIS_REPO environment
variable, defaulting to this machine's sibling checkout. This is inherently a
local tool (it reads a second repo on disk), not something CI can run.
"""
import os, re, sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import nt_overrides as ov

SITE = pathlib.Path(__file__).resolve().parent.parent
SVG  = SITE / 'covers' / 'SVG'

NOVATHESIS_REPO = pathlib.Path(os.environ.get(
    'NOVATHESIS_REPO',
    pathlib.Path.home() / 'LOCAL/Repos/Git/LaTeX/NOVAthesis/novathesis'))
SCHOOLS_CONF = NOVATHESIS_REPO / '.Build' / 'schools.conf'
SCHOOLS_DIR  = NOVATHESIS_REPO / 'novathesisFiles' / 'Schools'

GENERIC_LABELS = {
    'phd': ('PhD Dissertation', 'Dissertação de Doutoramento'),
    'msc': ('MSc Thesis', 'Tese de Mestrado'),
    'bsc': ('BSc Report', 'Relatório de Licenciatura'),
}

CONF_LINE = re.compile(r'^(\S+)\s+\[([^\]]+)\]\s+\[([^\]]+)\]')


def parse_schools_conf():
    """{path: {'doctypes': [...], 'langs': [...]}} from .Build/schools.conf."""
    if not SCHOOLS_CONF.exists():
        sys.exit(f'gen_nt_schools: {SCHOOLS_CONF} not found -- set NOVATHESIS_REPO')
    schools = {}
    for line in SCHOOLS_CONF.read_text(encoding='utf-8').splitlines():
        line = line.strip()
        if not line or line.startswith('#') or line.startswith('['):
            continue
        m = CONF_LINE.match(line)
        if not m:
            continue
        path, doctypes, langs = m.groups()
        schools[path] = dict(
            doctypes=[d.strip() for d in doctypes.split(',')],
            langs=[l.strip() for l in langs.split(',')])
    return schools


def find_clo(path):
    """The school's own -defaults.clo, wherever it actually lives (directory
    depth is inconsistent -- some multi-segment paths are files, not
    subfolders -- so this globs by filename instead of computing a directory)."""
    basename = path.replace('/', '-') + '-defaults.clo'
    matches = sorted(SCHOOLS_DIR.glob(f'**/{basename}'))
    return matches[0] if matches else None


INPUT_RE = re.compile(r'^[ \t]*\\input\{\\DIRSCHOOLS/(.+?)\}[ \t]*$', re.MULTILINE)


def resolve_clo_text(clo_path, _seen=None):
    """A .clo's own text, with any \\input{\\DIRSCHOOLS/...} lines it uses to
    pull in a shared parent file (e.g. nova/itqb/gray explicitly \\inputs
    nova/itqb/nova-itqb-defaults.clo for shared School/logo strings -- this is
    a manual chain some multi-variant schools use, not the standard two-file
    university+leaf load, so it has to be followed explicitly)."""
    if clo_path is None or not clo_path.exists():
        return ''
    _seen = _seen or set()
    if clo_path in _seen:
        return ''
    _seen.add(clo_path)
    text = clo_path.read_text(encoding='utf-8', errors='ignore')
    parts = []
    for m in INPUT_RE.finditer(text):
        target = SCHOOLS_DIR / m.group(1)
        if not target.suffix:
            target = target.with_suffix('.clo')
        parts.append(resolve_clo_text(target, _seen))
    parts.append(text)
    return '\n'.join(parts)


# Non-display-name keys that can precede a language code in this codebase,
# e.g. \SetSchool*(logo,en)={...} or \SetSchool*(logo,neg,pt)={...} for logo
# filenames. Excluded so the one-extra-segment allowance below (for
# \SetSchool*(isel,pt)={...}-style institution namespacing) doesn't also
# match these.
_NON_NAME_PREFIX = r'(?:logo|address|neg|RGB|GRAY)'


def _set_start_re(cmd, lang):
    # No '*' requirement: both \SetX(en)=... and \SetX*(en)=... occur. The key
    # is usually just (lang), but some schools namespace it, e.g.
    # \SetSchool*(isel,pt)={...} (ipl/isel, shared with its meb variant) --
    # so allow one leading segment before the language code, as long as it's
    # not a known non-name key. Anchoring to line-start (with MULTILINE)
    # keeps this from matching a commented-out example line like
    # "%   \SetSchool*(en)={...}".
    return re.compile(r'^[ \t]*\\Set' + re.escape(cmd) + r'\*?\((?!' + _NON_NAME_PREFIX +
                       r',)(?:[\w-]+,)?' + lang + r'\)=\{', re.MULTILINE)


def _read_braced_value(text, open_brace_pos):
    """Text of a {...} group starting at open_brace_pos, honouring nested
    braces (values like "\\emph{University}" have a '}' before the real end)."""
    depth = 0
    for i in range(open_brace_pos, len(text)):
        if text[i] == '{':
            depth += 1
        elif text[i] == '}':
            depth -= 1
            if depth == 0:
                return text[open_brace_pos + 1:i]
    return text[open_brace_pos + 1:]  # unterminated -- best effort


def _clean_latex(s):
    """LaTeX source -> plain text safe to inject into the generated HTML.

    Only handles what's actually observed in University/School strings across
    every .clo file: an escaped ampersand (must become the HTML entity, not
    the literal LaTeX escape) and a forced line break (rendered as a space --
    these names are used inline, e.g. "{uni} — {school}")."""
    return s.replace(r'\&', '&amp;').replace(r'\\', ' ').strip()


def extract_strings(clo_path, cmd):
    """{'en': ..., 'pt': ...} for \\Set<cmd>*(en|pt)={...} in one .clo file
    (plus anything it \\inputs -- see resolve_clo_text).

    Takes the *last* match per language, mirroring real \\Set... semantics
    (each call overwrites the previous one, so a later line wins). Mutually
    falls back when only one language is defined -- common for proper nouns
    (e.g. "Humboldt-Universität zu Berlin" has no PT variant)."""
    out = {'en': '', 'pt': ''}
    text = resolve_clo_text(clo_path)
    if not text:
        return out
    for lang in ('en', 'pt'):
        matches = [_read_braced_value(text, m.end() - 1)
                   for m in _set_start_re(cmd, lang).finditer(text)]
        if matches:
            out[lang] = _clean_latex(matches[-1])
    if out['en'] and not out['pt']:
        out['pt'] = out['en']
    elif out['pt'] and not out['en']:
        out['en'] = out['pt']
    return out


def university_and_school(path):
    """(uni_en, uni_pt), (school_en, school_pt) for one schools.conf path.

    Mirrors the real build (nt-setup.sty): only two .clo files are ever
    loaded for a document -- the university-level defaults, then the leaf's
    own -defaults.clo, which may itself override University."""
    univ_key = path.split('/', 1)[0]
    uni = extract_strings(SCHOOLS_DIR / univ_key / f'{univ_key}-defaults.clo', 'University')
    leaf_clo = find_clo(path)
    leaf_uni = extract_strings(leaf_clo, 'University')
    if leaf_uni['en']:
        uni = leaf_uni
    school = extract_strings(leaf_clo, 'School')
    return (uni['en'], uni['pt']), (school['en'], school['pt'])


def gen_institutions(conf):
    rows = []
    for inst in ov.INSTITUTIONS:
        uni = school = None
        blocks = []
        for p in inst['paths']:
            path = p['path']
            info = conf.get(path)
            if info is None:
                print(f"gen_nt_schools: {path!r} (institution {inst['key']!r}) not in "
                      f"schools.conf -- skipped", file=sys.stderr)
                continue
            this_uni, this_school = university_and_school(path)
            if uni is None:
                uni, school = this_uni, this_school
            lang = p.get('lang', 'en')
            stem_base = path.replace('/', '-')
            for doctype in info['doctypes']:
                stem = f'{stem_base}-{doctype}-{lang}-lua'
                if not (SVG / f'{stem}-1.svg').exists():
                    continue  # coverage gate: schools.conf lists it, but no art yet
                label = p.get('labels', {}).get(doctype) or GENERIC_LABELS.get(doctype)
                if label is None:
                    print(f"gen_nt_schools: {path!r} doctype {doctype!r} has cover art but "
                          f"no label (not phd/msc/bsc and no override) -- skipped",
                          file=sys.stderr)
                    continue
                blocks.append((stem, label[0], label[1]))
        if not blocks:
            print(f"gen_nt_schools: institution {inst['key']!r} has no cover art for any of "
                  f"its paths -- dropped entirely", file=sys.stderr)
            continue
        row = dict(key=inst['key'], uni=uni, school=school, tag=inst['tag'], blocks=blocks)
        if inst.get('credit'):
            row['credit'] = inst['credit']
        rows.append(row)
    return rows


def _fmt_tuple2(t):
    a, b = t
    return f'({a!r},) * 2' if a == b else f'({a!r}, {b!r})'


def render_institutions(rows):
    out = ['INSTITUTIONS = [']
    for r in rows:
        out.append(f" dict(key={r['key']!r}, uni={_fmt_tuple2(r['uni'])}, "
                   f"school={_fmt_tuple2(r['school'])},")
        credit = f", credit={r['credit']!r}" if r.get('credit') else ''
        out.append(f"      tag={r['tag']!r}{credit}, blocks=[")
        for stem, en, pt in r['blocks']:
            out.append(f"        ({stem!r}, {en!r}, {pt!r}),")
        out.append('      ]),')
        out.append('')
    if out[-1] == '':
        out.pop()
    out.append(']')
    return '\n'.join(out)


def render_repos():
    out = ['GROUPS = [']
    for g, label in ov.GROUPS:
        out.append(f' ({g!r}, {label!r}),')
    out.append(']')
    out.append('')
    out.append('REPOS = [')
    for r in ov.REPOS:
        parts = [f"group={r['group']!r}", f"repo={r['repo']!r}", f"label={r['label']!r}"]
        if r.get('cover'):
            parts.append(f"cover={r['cover']!r}")
        if r.get('crop'):
            parts.append('crop=True')
        out.append(f" dict({', '.join(parts)}),")
    out.append(']')
    return '\n'.join(out)


HELPERS = '''
ORG = 'https://github.com/novathesis'

def overleaf(repo):
    """Overleaf import URL: uploads the repo's main ZIP and sets the root document."""
    return (f'https://www.overleaf.com/docs?snip_uri={ORG}/{repo}'
            f'/archive/refs/heads/main.zip&amp;main_document=template.tex')

def find(stem, page):
    """Resolve stem-page.svg, tolerating an export-tool page suffix (-N-1.svg)."""
    exact = SVG / f'{stem}-{page}.svg'
    if exact.exists():
        return exact
    extra = sorted(SVG.glob(f'{stem}-{page}-[0-9].svg'))
    return extra[0] if extra else None

def ratio(path):
    """width/height from the SVG viewBox; >1 means a wrap-around cover."""
    head = path.read_text(encoding='utf-8', errors='ignore')[:600]
    m = re.search(r'viewBox="0 0 ([\\d.]+) ([\\d.]+)"', head)
    return float(m.group(1)) / float(m.group(2)) if m else 0.707

def cover_stem(r):
    """The asset stem for a repository card.

    'cover' is optional: when absent it is derived from the repository name, so
    a new school usually needs only group/repo/label. uminho resolves to
    uminho-eeng-phd-en-lua this way.
    """
    if r.get('cover'):
        return r['cover']
    found = sorted(SVG.glob(f"{r['repo']}-*-1.svg")) + sorted(SVG.glob(f"{r['repo']}-*-1-[0-9].svg"))
    stems = [re.sub(r'-1(-\\d)?\\.svg$', '', f.name) for f in found]
    if not stems:
        return None
    phd = [s for s in stems if '-phd-' in s]
    return (phd or stems)[0]

def validate():
    """Check the registry against the files on disk. Returns a list of problems."""
    problems = []
    seen = set()
    for r in REPOS:
        for field in ('group', 'repo', 'label'):
            if not r.get(field):
                problems.append(f"REPOS entry {r!r}: missing {field!r}")
        if r.get('repo') in seen:
            problems.append(f"REPOS: duplicate repo {r['repo']!r}")
        seen.add(r.get('repo'))
        if r.get('group') not in {g for g, _ in GROUPS}:
            problems.append(f"{r.get('repo')}: unknown group {r.get('group')!r}")
        stem = cover_stem(r)
        if not stem:
            problems.append(f"{r.get('repo')}: no cover found -- set cover=, "
                            f"or add covers/SVG/{r.get('repo')}-<degree>-en-lua-1.svg")
        elif not find(stem, '1'):
            problems.append(f"{r.get('repo')}: cover {stem}-1.svg not found")
    for inst in INSTITUTIONS:
        for stem, *_ in inst['blocks']:
            if not any(find(stem, p) for p in ('N', '1', '2', 'L1')):
                problems.append(f"{inst['key']}: block {stem} has no pages at all")
    return problems

def check_or_exit():
    problems = validate()
    if problems:
        import sys
        print('nt_schools.py: the registry does not match the files on disk\\n', file=sys.stderr)
        for p in problems:
            print(f'  - {p}', file=sys.stderr)
        sys.exit(1)
'''

HEADER = '''"""Single source of truth for the school data behind showcase.html and schools.html.

GENERATED FILE -- do not hand-edit. Edit tools/nt_overrides.py, then run:

    python3 tools/gen_nt_schools.py
    python3 tools/gen_showcase.py
    python3 tools/gen_findyourschool.py

University/school display names and which doctypes have cover art are derived
from the sibling novathesis repo's .Build/schools.conf and
novathesisFiles/Schools/**/*.clo (see gen_nt_schools.py). Tag, credit, GROUPS,
REPOS, and custom per-degree block labels come from nt_overrides.py, which has
no mechanical source and is meant to be hand-edited.
"""
import re, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
SVG  = SITE / 'covers' / 'SVG'

'''


def main():
    conf = parse_schools_conf()
    rows = gen_institutions(conf)
    out = [HEADER.rstrip(), '', render_institutions(rows), '', render_repos(), HELPERS.rstrip('\n')]
    (SITE / 'tools' / 'nt_schools.py').write_text('\n'.join(out) + '\n', encoding='utf-8')
    print('tools/nt_schools.py: written')


if __name__ == '__main__':
    main()
