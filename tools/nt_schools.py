"""Single source of truth for the school data behind showcase.html and schools.html.

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
import re, pathlib, urllib.parse

SITE = pathlib.Path(__file__).resolve().parent.parent
SVG  = SITE / 'covers' / 'SVG'

INSTITUTIONS = [
 dict(key='manual', uni=('\\emph{University}', '\\emph{Universidade}'), school=('\\emph{School}', '\\emph{Faculdade}'),
      tag='novathesis', blocks=[
        ('other-novathesis-phd-en-lua', 'The <b>nova</b>thesis manual', 'O manual <b>nova</b>thesis'),
      ]),

 dict(key='nova-fct', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'), school=('NOVA School of Science and Technology', 'Faculdade de Ciências e Tecnologia'),
      tag='NOVA FCT', blocks=[
        ('nova-fct-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
        ('nova-fct-msc-en-lua', 'MSc Thesis', 'Tese de Mestrado'),
        ('nova-fct-cbbi-msc-en-lua', 'MSc in Computational Biology &amp; Bioinformatics', 'Mestrado em Biologia Computacional &amp; Bioinformática'),
        ('nova-fct-di-adc-bsc-en-lua', 'BSc in Computer Science', 'Licenciatura em Informática'),
      ]),

 dict(key='nova-fcsh', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'), school=('School of Social Sciences and Humanities', 'Faculdade de Ciências Sociais e Humanas'),
      tag='NOVA FCSH', blocks=[
        ('nova-fcsh-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='nova-itqb', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'), school=('Instituto de Tecnologia Química e Biológica António Xavier',) * 2,
      tag='NOVA ITQB', blocks=[
        ('nova-itqb-gray-phd-en-lua', 'PhD Dissertation — Gray', 'Dissertação de Doutoramento — Cinza'),
        ('nova-itqb-green-phd-en-lua', 'PhD Dissertation — Green', 'Dissertação de Doutoramento — Verde'),
      ]),

 dict(key='nova-ims', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'), school=('Information Management School',) * 2,
      tag='NOVA IMS', credit=('Paulo Vitor de Campos Souza', 'pdecampossouza'), blocks=[
        ('nova-ims-msc-en-lua', 'MSc Thesis', 'Tese de Mestrado'),
      ]),

 dict(key='nova-ensp', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'), school=('National School of Public Health', 'Escola Nacional de Saúde Pública'),
      tag='NOVA ENSP', blocks=[
        ('nova-ensp-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulisboa-ist', uni=('Universidade de Lisboa',) * 2, school=('Instituto Superior Técnico',) * 2,
      tag='ULISBOA IST', blocks=[
        ('ulisboa-ist-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulisboa-fcul', uni=('Universidade de Lisboa',) * 2, school=('Faculty of Sciences', 'Faculdade de Ciências'),
      tag='ULISBOA FCUL', credit=('Martim Costa Seco', ''), blocks=[
        ('ulisboa-fcul-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulisboa-iseg', uni=('Universidade de Lisboa',) * 2, school=('Lisbon School of Economics &amp; Management', 'Instituto Superior de Economia e Gestão'),
      tag='ULISBOA ISEG', blocks=[
        ('ulisboa-iseg-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulisboa-fmv', uni=('Universidade de Lisboa',) * 2, school=('Faculty of Veterinary Medicine', 'Faculdade de Medicina Veterinária'),
      tag='ULISBOA FMV', blocks=[
        ('ulisboa-fmv-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulisboa-fful', uni=('Universidade de Lisboa',) * 2, school=('Faculty of Pharmacy', 'Faculdade de Farmácia'),
      tag='ULISBOA FFUL', credit=('Afonso Nóbrega', 'nobrega8'), blocks=[
        ('ulisboa-fful-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='uminho', uni=('Universidade do Minho',) * 2, school=('School of Engineering', 'Escola de Engenharia'),
      tag='UMINHO', credit=('Bruno Pereira', 'b-pereira'), blocks=[
        ('uminho-eeng-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
        ('uminho-eeng-msc-en-lua', 'MSc Thesis', 'Tese de Mestrado'),
      ]),

 dict(key='iscteiul-eta', uni=('Iscte – University Institute of Lisbon', 'Iscte — Instituto Universitário de Lisboa'), school=('School of Technology and Architecture', 'Escola de Tecnologia e Arquitectura'),
      tag='ISCTE-IUL ETA', blocks=[
        ('iscteiul-eta-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulht-deisi', uni=('Universidade Lusófona de Humanidades e Tecnologias',) * 2, school=('Departamento de Engenharia Informática e Sistemas de Informação',) * 2,
      tag='ULHT DEISI', blocks=[
        ('ulht-deisi-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ulht-mge', uni=('Universidade Lusófona de Humanidades e Tecnologias',) * 2, school=('Escola de Ciências Econômicas e das Organizações',) * 2,
      tag='ULHT MGE', blocks=[
        ('ulht-mge-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='uporto-fcup', uni=('Universidade do Porto',) * 2, school=('Faculdade de Ciências',) * 2,
      tag='UPORTO FCUP', credit=('Guilherme Borges', 'sgtpepperpt'), blocks=[
        ('uporto-fcup-phd-en-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),

 dict(key='ipl-isel', uni=('Instituto Politécnico de Lisboa',) * 2, school=('Instituto Superior de Engenharia de Lisboa',) * 2,
      tag='IPL ISEL', credit=('Gonçalo N. Duarte', 'MrDuartePT'), blocks=[
        ('ipl-isel-msc-en-lua', 'MSc Thesis', 'Tese de Mestrado'),
        ('ipl-isel-meb-msc-en-lua', 'MSc in Biomedical Engineering', 'Mestrado em Engenharia Biomédica'),
      ]),

 dict(key='ips-ests', uni=('Polytechnic Institute of Setúbal', 'Instituto Politécnico de Setúbal'), school=('Escola Superior de Tecnologia de Setúbal',) * 2,
      tag='IPS ESTS', blocks=[
        ('ips-ests-msc-en-lua', 'MSc Thesis', 'Tese de Mestrado'),
      ]),

 dict(key='other-esep', uni=('Nursing School of Porto', 'Escola Superior de Enfermagem do Porto'), school=('Nursing School of Porto', 'Escola Superior de Enfermagem do Porto'),
      tag='ESEP', blocks=[
        ('other-esep-msc-en-lua', 'MSc Thesis', 'Tese de Mestrado'),
      ]),

 dict(key='other-huberlin', uni=('Humboldt-Universität zu Berlin',) * 2, school=('Institute of Library and Information Science',) * 2,
      tag='HU BERLIN', blocks=[
        ('other-huberlin-phd-de-lua', 'PhD Dissertation', 'Dissertação de Doutoramento'),
      ]),
]

GROUPS = [
 ('nova', 'Universidade NOVA de Lisboa'),
 ('ul', 'Universidade de Lisboa'),
 ('other', ' · Porto · Minho · Lusófona · ISCTE · Politécnicos · outras'),
]

REPOS = [
 dict(group='nova', repo='nova-fct', label='Faculdade de Ciências e Tecnologia (NOVA FCT)', cover='nova-fct-phd-en-lua'),
 dict(group='nova', repo='nova-fct-cbbi', label='NOVA FCT — CBBI', cover='nova-fct-cbbi-msc-en-lua'),
 dict(group='nova', repo='nova-fct-di-adc', label='NOVA FCT — DI-ADC', cover='nova-fct-di-adc-bsc-en-lua'),
 dict(group='nova', repo='nova-ensp', label='Escola Nacional de Saúde Pública (ENSP)', cover='nova-ensp-phd-en-lua'),
 dict(group='nova', repo='nova-itqb', label='Instituto de Tecnologia Química e Biológica (ITQB)', cover='nova-itqb-green-phd-en-lua'),
 dict(group='nova', repo='nova-fcsh', label='Faculdade de Ciências Sociais e Humanas (FCSH)', cover='nova-fcsh-phd-en-lua'),
 dict(group='nova', repo='nova-ims', label='NOVA Information Management School (NOVA IMS)', cover='nova-ims-msc-en-lua', org='https://github.com/pdecampossouza', slug='nova-ims-thesis-template-2025', zip='NOVAthesis 2025-2026.zip'),
 dict(group='ul', repo='ulisboa-fcul', label='Faculdade de Ciências, ULisboa (FCUL)', cover='ulisboa-fcul-phd-en-lua'),
 dict(group='ul', repo='ulisboa-ist', label='Instituto Superior Técnico (IST)'),
 dict(group='ul', repo='ulisboa-iseg', label='Instituto Superior de Economia e Gestão (ISEG)', cover='ulisboa-iseg-phd-en-lua'),
 dict(group='ul', repo='ulisboa-fmv', label='Faculdade de Medicina Veterinária (FMV)', cover='ulisboa-fmv-phd-en-lua'),
 dict(group='ul', repo='ulisboa-fful', label='Faculdade de Farmácia (FFUL)', cover='ulisboa-fful-phd-en-lua'),
 dict(group='other', repo='uporto-fcup', label='Faculdade de Ciências, UPorto (FCUP)', cover='uporto-fcup-phd-en-lua'),
 dict(group='other', repo='uminho', label='Universidade do Minho', crop=True),
 dict(group='other', repo='ulht-deisi', label='Universidade Lusófona — DEISI', cover='ulht-deisi-phd-en-lua'),
 dict(group='other', repo='ulht-mge', label='Universidade Lusófona — MGE', cover='ulht-mge-phd-en-lua'),
 dict(group='other', repo='iscteiul-eta', label='ISCTE-IUL — ETA', cover='iscteiul-eta-phd-en-lua'),
 dict(group='other', repo='ipl-isel', label='Instituto Superior de Engenharia de Lisboa (ISEL)', cover='ipl-isel-msc-en-lua'),
 dict(group='other', repo='ips-ests', label='Escola Superior de Tecnologia de Setúbal (ESTS)', cover='ips-ests-msc-en-lua'),
 dict(group='other', repo='other-esep', label='Escola Superior de Enfermagem do Porto (ESEP)', cover='other-esep-msc-en-lua'),
 dict(group='other', repo='other-huberlin', label='Humboldt-Universität zu Berlin (HU Berlin)', cover='other-huberlin-phd-de-lua'),
]

ORG = 'https://github.com/novathesis'

# Showcase rows that are deliberately not repository cards. The manual is not a
# school, so it has no "Find your school" entry and must not be reported as a
# gap. Everything else on the showcase needs a card.
SHOWCASE_ONLY = {'manual'}

def external(key):
    """The REPOS entry for a showcase row whose repository lives outside the
    novathesis organisation, or None. Derived from `org`, so the showcase and
    the "Find your school" card cannot disagree about what is external."""
    for r in REPOS:
        if r['repo'] == key and r.get('org'):
            return r
    return None

def repo_url(r):
    """The repository's GitHub page. `org` and `slug` cover a school whose
    template lives outside the novathesis organisation, under its own name."""
    return f"{r.get('org', ORG)}/{r.get('slug', r['repo'])}"

def zip_url(r):
    """The ZIP a reader should download, and the one Overleaf should import.
    `zip` names a ZIP committed inside the repository, for a repo that ships the
    template packaged instead of as a source tree: importing such a repo's own
    archive would nest one ZIP inside another, and neither a reader nor Overleaf
    would find template.tex at the top level."""
    branch = r.get('branch', 'main')
    if r.get('zip'):
        return f"{repo_url(r)}/raw/{branch}/{urllib.parse.quote(r['zip'])}"
    return f'{repo_url(r)}/archive/refs/heads/{branch}.zip'

def overleaf(r):
    """Overleaf import URL: uploads the template ZIP and sets the root document."""
    return (f'https://www.overleaf.com/docs?snip_uri={zip_url(r)}'
            f'&amp;main_document=template.tex')

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
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
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
    stems = [re.sub(r'-1(-\d)?\.svg$', '', f.name) for f in found]
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
        for field in ('org', 'slug', 'zip', 'branch'):
            if field in r and not r[field]:
                problems.append(f"{r.get('repo')}: {field!r} is present but empty")
    # A showcase row with no card is invisible on "Find your school", which is
    # silent and easy to miss. The reverse is legitimate and not checked: one
    # repo can serve many showcase paths (uminho's covers 12 sub-schools), and
    # one showcase row can merge several repos (nova-fct spans three).
    cards = {r['repo'] for r in REPOS}
    for inst in INSTITUTIONS:
        for stem, *_ in inst['blocks']:
            if not any(find(stem, p) for p in ('N', '1', '2', 'L1')):
                problems.append(f"{inst['key']}: block {stem} has no pages at all")
        if inst['key'] not in cards and inst['key'] not in SHOWCASE_ONLY:
            problems.append(f"{inst['key']}: on the showcase but has no REPOS card -- "
                            f"add one in nt_overrides.py, or list the key in SHOWCASE_ONLY")
    return problems

def check_or_exit():
    problems = validate()
    if problems:
        import sys
        print('nt_schools.py: the registry does not match the files on disk\n', file=sys.stderr)
        for p in problems:
            print(f'  - {p}', file=sys.stderr)
        sys.exit(1)
