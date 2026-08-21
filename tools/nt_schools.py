"""Single source of truth for the school data behind showcase.html and schools.html.

Edit this file when a school is added, renamed, or gains a contributor; then run
both generators:

    python3 tools/gen_showcase.py
    python3 tools/gen_findyourschool.py

Three identifiers are deliberately kept apart, because they do not always agree:

    key     the institution, and the showcase section it heads
    assets  the stem of the cover files in covers/SVG
    repo    the repository under github.com/novathesis

uminho is the clearest example -- one repository, assets named after the
Engineering school. ulisboa-ff is another: the school is branded FFUL while its
files and repository are still named ff.
"""
import re, pathlib

SITE = pathlib.Path(__file__).resolve().parent.parent
SVG  = SITE / 'covers' / 'SVG'

PHD = ('PhD Dissertation', 'Dissertação de Doutoramento')
MSC = ('MSc Thesis', 'Tese de Mestrado')

# ─────────────────────────────────────────────────────────────────────────────
# Institutions, in showcase order. blocks = (asset stem, label_en, label_pt).
# credit = (name, github handle); the handle may be empty.
# ─────────────────────────────────────────────────────────────────────────────
INSTITUTIONS = [
 dict(key='manual', uni=('', ''), school=('', ''), tag='novathesis',
      blocks=[('other-novathesis-phd-en-lua',
               'The <b>nova</b>thesis manual', 'O manual <b>nova</b>thesis')]),

 dict(key='nova-fct', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'),
      school=('NOVA School of Science and Technology', 'Faculdade de Ciências e Tecnologia'),
      tag='NOVA FCT', blocks=[
        ('nova-fct-phd-en-lua', *PHD),
        ('nova-fct-msc-en-lua', *MSC),
        ('nova-fct-cbbi-msc-en-lua', 'MSc in Computational Biology &amp; Bioinformatics',
                                     'Mestrado em Biologia Computacional &amp; Bioinformática'),
        ('nova-fct-di-adc-bsc-en-lua', 'BSc in Computer Science', 'Licenciatura em Informática')]),

 dict(key='nova-fcsh', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'),
      school=('School of Social Sciences and Humanities', 'Faculdade de Ciências Sociais e Humanas'),
      tag='NOVA FCSH', blocks=[('nova-fcsh-phd-en-lua', *PHD)]),

 dict(key='nova-itqb', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'),
      school=('Instituto de Tecnologia Química e Biológica António Xavier',) * 2,
      tag='NOVA ITQB', blocks=[
        ('nova-itqb-gray-phd-en-lua',  'PhD Dissertation — Gray',  'Dissertação de Doutoramento — Cinza'),
        ('nova-itqb-green-phd-en-lua', 'PhD Dissertation — Green', 'Dissertação de Doutoramento — Verde')]),

 dict(key='nova-ensp', uni=('NOVA University Lisbon', 'Universidade NOVA de Lisboa'),
      school=('National School of Public Health', 'Escola Nacional de Saúde Pública'),
      tag='NOVA ENSP', blocks=[('nova-ensp-phd-en-lua', *PHD)]),

 dict(key='ulisboa-ist', uni=('Universidade de Lisboa',) * 2,
      school=('Instituto Superior Técnico',) * 2,
      tag='ULISBOA IST', blocks=[('ulisboa-ist-phd-en-lua', *PHD)]),

 dict(key='ulisboa-fcul', uni=('Universidade de Lisboa',) * 2,
      school=('Faculty of Sciences', 'Faculdade de Ciências'), tag='ULISBOA FCUL',
      credit=('Martim Costa Seco', ''), blocks=[('ulisboa-fcul-phd-en-lua', *PHD)]),

 dict(key='ulisboa-iseg', uni=('Universidade de Lisboa',) * 2,
      school=('Lisbon School of Economics &amp; Management', 'Instituto Superior de Economia e Gestão'),
      tag='ULISBOA ISEG', blocks=[('ulisboa-iseg-phd-en-lua', *PHD)]),

 dict(key='ulisboa-fmv', uni=('Universidade de Lisboa',) * 2,
      school=('Faculty of Veterinary Medicine', 'Faculdade de Medicina Veterinária'),
      tag='ULISBOA FMV', blocks=[('ulisboa-fmv-phd-en-lua', *PHD)]),

 dict(key='ulisboa-ff', uni=('Universidade de Lisboa',) * 2,
      school=('Faculty of Pharmacy', 'Faculdade de Farmácia'), tag='ULISBOA FFUL',
      credit=('Afonso Nóbrega', 'nobrega8'), blocks=[('ulisboa-ff-phd-en-lua', *PHD)]),

 dict(key='uminho', uni=('Universidade do Minho',) * 2,
      school=('School of Engineering', 'Escola de Engenharia'), tag='UMINHO',
      credit=('Bruno Pereira', 'b-pereira'), blocks=[('uminho-eeng-phd-en-lua', *PHD)]),

 dict(key='iscteiul-eta', uni=('Iscte – University Institute of Lisbon',
                               'Iscte — Instituto Universitário de Lisboa'),
      school=('School of Technology and Architecture', 'Escola de Tecnologia e Arquitectura'),
      tag='ISCTE-IUL ETA', blocks=[('iscteiul-eta-phd-en-lua', *PHD)]),

 dict(key='ulht-deisi', uni=('Universidade Lusófona de Humanidades e Tecnologias',) * 2,
      school=('Departamento de Engenharia Informática e Sistemas de Informação',) * 2,
      tag='ULHT DEISI', blocks=[('ulht-deisi-phd-en-lua', *PHD)]),

 dict(key='ulht-mge', uni=('Universidade Lusófona de Humanidades e Tecnologias',) * 2,
      school=('Escola de Ciências Econômicas e das Organizações',) * 2,
      tag='ULHT MGE', blocks=[('ulht-mge-phd-en-lua', *PHD)]),

 dict(key='uporto-fcup', uni=('Universidade do Porto',) * 2,
      school=('Faculdade de Ciências',) * 2, tag='UPORTO FCUP',
      credit=('Guilherme Borges', 'sgtpepperpt'), blocks=[('uporto-fcup-phd-en-lua', *PHD)]),

 dict(key='ipl-isel', uni=('Instituto Politécnico de Lisboa',) * 2,
      school=('Instituto Superior de Engenharia de Lisboa',) * 2, tag='IPL ISEL',
      credit=('Gonçalo N. Duarte', 'MrDuartePT'), blocks=[
        ('ipl-isel-msc-en-lua', *MSC),
        ('ipl-isel-meb-msc-en-lua', 'MSc in Biomedical Engineering',
                                    'Mestrado em Engenharia Biomédica')]),

 dict(key='ips-ests', uni=('Polytechnic Institute of Setúbal', 'Instituto Politécnico de Setúbal'),
      school=('Escola Superior de Tecnologia de Setúbal',) * 2,
      tag='IPS ESTS', blocks=[('ips-ests-msc-en-lua', *MSC)]),

 dict(key='other-esep', uni=('Nursing School of Porto', 'Escola Superior de Enfermagem do Porto'),
      school=('', ''), tag='ESEP', blocks=[('other-esep-msc-en-lua', *MSC)]),
]

# ─────────────────────────────────────────────────────────────────────────────
# Repository cards for "Find your school", in page order. One card per repo, so
# this is finer-grained than INSTITUTIONS (NOVA FCT ships three repositories).
# label is the same in both languages. cover is the asset shown on the card.
# ─────────────────────────────────────────────────────────────────────────────
GROUPS = [
 ('nova',  'Universidade NOVA de Lisboa'),
 ('ulpm',  'Universidade de Lisboa · Porto · Minho'),
 ('other', 'Lusófona · ISCTE · Politécnicos · outras'),
]

REPOS = [
 dict(group='nova',  repo='nova-fct',        label='Ciências e Tecnologia (NOVA FCT)',  cover='nova-fct-phd-en-lua'),
 dict(group='nova',  repo='nova-fct-cbbi',   label='NOVA FCT — CBBI',                   cover='nova-fct-cbbi-msc-en-lua'),
 dict(group='nova',  repo='nova-fct-di-adc', label='NOVA FCT — DI-ADC',                 cover='nova-fct-di-adc-bsc-en-lua'),
 dict(group='nova',  repo='nova-ensp',       label='Saúde Pública (ENSP)',              cover='nova-ensp-phd-en-lua'),
 dict(group='nova',  repo='nova-itqb',       label='Química e Biológica (ITQB)',        cover='nova-itqb-green-phd-en-lua'),
 dict(group='nova',  repo='nova-fcsh',       label='Ciências Sociais e Humanas (FCSH)', cover='nova-fcsh-phd-en-lua'),

 dict(group='ulpm',  repo='ulisboa-fcul',    label='Faculdade de Ciências (FCUL)',      cover='ulisboa-fcul-phd-en-lua'),
 dict(group='ulpm',  repo='ulisboa-ist',     label='Instituto Superior Técnico (IST)',  cover='ulisboa-ist-phd-en-lua'),
 dict(group='ulpm',  repo='ulisboa-iseg',    label='Economia e Gestão (ISEG)',          cover='ulisboa-iseg-phd-en-lua'),
 dict(group='ulpm',  repo='ulisboa-fmv',     label='Medicina Veterinária (FMV)',        cover='ulisboa-fmv-phd-en-lua'),
 dict(group='ulpm',  repo='ulisboa-ff',      label='Farmácia (FFUL)',                   cover='ulisboa-ff-phd-en-lua'),
 dict(group='ulpm',  repo='uporto-fcup',     label='Ciências, UPorto (FCUP)',           cover='uporto-fcup-phd-en-lua'),
 dict(group='ulpm',  repo='uminho',          label='Universidade do Minho',             cover='uminho-eeng-phd-en-lua', crop=True),

 dict(group='other', repo='ulht-deisi',      label='Lusófona — DEISI',                  cover='ulht-deisi-phd-en-lua'),
 dict(group='other', repo='ulht-mge',        label='Lusófona — MGE',                    cover='ulht-mge-phd-en-lua'),
 dict(group='other', repo='iscteiul-eta',    label='ISCTE-IUL — ETA',                   cover='iscteiul-eta-phd-en-lua'),
 dict(group='other', repo='ipl-isel',        label='ISEL, IPL',                         cover='ipl-isel-msc-en-lua'),
 dict(group='other', repo='ips-ests',        label='ESTSetúbal, IPS',                   cover='ips-ests-msc-en-lua'),
 dict(group='other', repo='other-esep',      label='Enfermagem do Porto (ESEP)',        cover='other-esep-msc-en-lua'),
]

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
    m = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', head)
    return float(m.group(1)) / float(m.group(2)) if m else 0.707
