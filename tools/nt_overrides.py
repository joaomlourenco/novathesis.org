"""Hand-curated data with no source of truth in the novathesis LaTeX repo.

Edit this file when a school is added, dropped, renamed, or gains a
contributor -- then regenerate:

    python3 tools/gen_nt_schools.py
    python3 tools/gen_showcase.py
    python3 tools/gen_findyourschool.py

Bilingual university/school names and which doctypes actually have cover art
are derived automatically from the sibling novathesis repo's
.Build/schools.conf and novathesisFiles/Schools/**/*.clo files (see
gen_nt_schools.py). Everything below is editorial and cannot be derived:

INSTITUTIONS
    One entry per showcase row. `paths` lists the schools.conf path(s) it
    aggregates (e.g. nova-fct's row spans three paths: nova/fct,
    nova/fct/cbbi, nova/fct/di-adc). Each path entry may set:
        labels  {doctype: (label_en, label_pt)} -- overrides the generic
                PhD/MSc/BSc label for that doctype; omit to use the generic one
        lang    asset-language token (default 'en'); other/huberlin is 'de'
                because its cover is German-only, matching the school's own
                cover-language convention
    `tag` and `credit` apply to the whole row.

GROUPS / REPOS
    "Find your school" cards. One GitHub repo can serve several schools.conf
    paths (uminho's repo covers 12 sub-schools; ipl-isel's covers 2), so this
    stays a flat, fully hand-curated list -- gen_nt_schools.py copies it into
    nt_schools.py unchanged. cover_stem() in nt_schools.py already derives the
    cover asset from `repo` when `cover` is omitted.
"""

INSTITUTIONS = [
    dict(key='manual', tag='novathesis', paths=[
        dict(path='other/novathesis', labels={
            'phd': ('The <b>nova</b>thesis manual', 'O manual <b>nova</b>thesis')})]),

    dict(key='nova-fct', tag='NOVA FCT', paths=[
        dict(path='nova/fct'),
        dict(path='nova/fct/cbbi', labels={
            'msc': ('MSc in Computational Biology &amp; Bioinformatics',
                     'Mestrado em Biologia Computacional &amp; Bioinformática')}),
        dict(path='nova/fct/di-adc', labels={
            'bsc': ('BSc in Computer Science', 'Licenciatura em Informática')})]),

    dict(key='nova-fcsh', tag='NOVA FCSH', paths=[dict(path='nova/fcsh')]),

    dict(key='nova-itqb', tag='NOVA ITQB', paths=[
        dict(path='nova/itqb/gray', labels={
            'phd': ('PhD Dissertation — Gray', 'Dissertação de Doutoramento — Cinza')}),
        dict(path='nova/itqb/green', labels={
            'phd': ('PhD Dissertation — Green', 'Dissertação de Doutoramento — Verde')})]),

    dict(key='nova-ensp', tag='NOVA ENSP', paths=[dict(path='nova/ensp')]),

    dict(key='ulisboa-ist', tag='ULISBOA IST', paths=[dict(path='ulisboa/ist')]),

    dict(key='ulisboa-fcul', tag='ULISBOA FCUL', credit=('Martim Costa Seco', ''),
         paths=[dict(path='ulisboa/fcul')]),

    dict(key='ulisboa-iseg', tag='ULISBOA ISEG', paths=[dict(path='ulisboa/iseg')]),

    dict(key='ulisboa-fmv', tag='ULISBOA FMV', paths=[dict(path='ulisboa/fmv')]),

    dict(key='ulisboa-fful', tag='ULISBOA FFUL', credit=('Afonso Nóbrega', 'nobrega8'),
         paths=[dict(path='ulisboa/fful')]),

    dict(key='uminho', tag='UMINHO', credit=('Bruno Pereira', 'b-pereira'),
         paths=[dict(path='uminho/eeng')]),

    dict(key='iscteiul-eta', tag='ISCTE-IUL ETA', paths=[dict(path='iscteiul/eta')]),

    dict(key='ulht-deisi', tag='ULHT DEISI', paths=[dict(path='ulht/deisi')]),

    dict(key='ulht-mge', tag='ULHT MGE', paths=[dict(path='ulht/mge')]),

    dict(key='uporto-fcup', tag='UPORTO FCUP', credit=('Guilherme Borges', 'sgtpepperpt'),
         paths=[dict(path='uporto/fcup')]),

    dict(key='ipl-isel', tag='IPL ISEL', credit=('Gonçalo N. Duarte', 'MrDuartePT'), paths=[
        dict(path='ipl/isel'),
        dict(path='ipl/isel/meb', labels={
            'msc': ('MSc in Biomedical Engineering', 'Mestrado em Engenharia Biomédica')})]),

    dict(key='ips-ests', tag='IPS ESTS', paths=[dict(path='ips/ests')]),

    dict(key='other-esep', tag='ESEP', paths=[dict(path='other/esep')]),

    dict(key='other-huberlin', tag='HU BERLIN',
         paths=[dict(path='other/huberlin', lang='de')]),
]

GROUPS = [
    ('nova',  'Universidade NOVA de Lisboa'),
    ('ul',    'Universidade de Lisboa'),
    ('other', ' · Porto · Minho · Lusófona · ISCTE · Politécnicos · outras'),
]

REPOS = [
    dict(group='nova', repo='nova-fct',        label='Faculdade de Ciências e Tecnologia (NOVA FCT)', cover='nova-fct-phd-en-lua'),
    dict(group='nova', repo='nova-fct-cbbi',   label='NOVA FCT — CBBI',                                cover='nova-fct-cbbi-msc-en-lua'),
    dict(group='nova', repo='nova-fct-di-adc', label='NOVA FCT — DI-ADC',                              cover='nova-fct-di-adc-bsc-en-lua'),
    dict(group='nova', repo='nova-ensp',       label='Escola Nacional de Saúde Pública (ENSP)',        cover='nova-ensp-phd-en-lua'),
    dict(group='nova', repo='nova-itqb',       label='Instituto de Tecnologia Química e Biológica (ITQB)', cover='nova-itqb-green-phd-en-lua'),
    dict(group='nova', repo='nova-fcsh',       label='Faculdade de Ciências Sociais e Humanas (FCSH)', cover='nova-fcsh-phd-en-lua'),

    dict(group='ul', repo='ulisboa-fcul', label='Faculdade de Ciências, ULisboa (FCUL)',     cover='ulisboa-fcul-phd-en-lua'),
    dict(group='ul', repo='ulisboa-ist',  label='Instituto Superior Técnico (IST)'),
    dict(group='ul', repo='ulisboa-iseg', label='Instituto Superior de Economia e Gestão (ISEG)', cover='ulisboa-iseg-phd-en-lua'),
    dict(group='ul', repo='ulisboa-fmv',  label='Faculdade de Medicina Veterinária (FMV)',   cover='ulisboa-fmv-phd-en-lua'),
    dict(group='ul', repo='ulisboa-fful', label='Faculdade de Farmácia (FFUL)',              cover='ulisboa-fful-phd-en-lua'),

    dict(group='other', repo='uporto-fcup',    label='Faculdade de Ciências, UPorto (FCUP)',        cover='uporto-fcup-phd-en-lua'),
    dict(group='other', repo='uminho',         label='Universidade do Minho', crop=True),
    dict(group='other', repo='ulht-deisi',     label='Universidade Lusófona — DEISI',               cover='ulht-deisi-phd-en-lua'),
    dict(group='other', repo='ulht-mge',       label='Universidade Lusófona — MGE',                 cover='ulht-mge-phd-en-lua'),
    dict(group='other', repo='iscteiul-eta',   label='ISCTE-IUL — ETA',                             cover='iscteiul-eta-phd-en-lua'),
    dict(group='other', repo='ipl-isel',       label='Instituto Superior de Engenharia de Lisboa (ISEL)', cover='ipl-isel-msc-en-lua'),
    dict(group='other', repo='ips-ests',       label='Escola Superior de Tecnologia de Setúbal (ESTS)',   cover='ips-ests-msc-en-lua'),
    dict(group='other', repo='other-esep',     label='Escola Superior de Enfermagem do Porto (ESEP)',     cover='other-esep-msc-en-lua'),
    dict(group='other', repo='other-huberlin', label='Humboldt-Universität zu Berlin (HU Berlin)',        cover='other-huberlin-phd-de-lua'),
]
