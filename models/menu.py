#!/usr/bin/env python
# -*- coding: utf-8 -*-

response.logo = A(IMG(_src=URL('static', 'images/shebanq_logo_small.png')),
                  _class="brand",
                  _href=URL('default', 'index'),
                  _title='Home page',
                  _style="margin-bottom: -2em;",
                  )

response.logo2 = A(IMG(_src=URL('static', 'images/etcbc-round-small.png')),
                  _class="brand",
                  _href="http://www.etcbc.nl",
                  _title="to the ETCBC website",
                  _target="_blank",
                  _style="margin-bottom: -2em;",
                  )

served_on = request.env.SERVER_NAME
on_system = False
on_local = False
on_prod = False
on_devel = False
if served_on == None: on_system = True
elif served_on.endswith('local'): on_local = True
elif served_on == 'shebanq.ancient-data.org': on_prod = True
else: on_devel = True

#response.title = request.application.replace('_',' ').title()
response.title = request.function.replace('_', ' ').capitalize()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'SHEBANQ <shebanq@ancient-data.org>'
response.meta.description = 'Search engine for biblical Hebrew based on the Biblia Hebraica Stuttgartensia (Amstelodamensis) database (formerly known as ETCBC, historically known as WIVU)'
response.meta.keywords = 'Hebrew, Text Database, Bible, Query, Annotation, Online Hebrew Bible, Online Bible Hebrew, Hebrew Online Bible, Hebrew Bible Reader, Hebrew Bible Search, Hebrew Bible Research, Data Science, Text Database, Linguistic Queries, WIVU, ETCBC, BHS, BHSA, Biblia Hebraica, Biblia Hebraica Stuttgartensia, Biblia Hebraica Stuttgartensia Amstelodamensis'
response.meta.generator = 'BHSA Data'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    ('' if on_prod else served_on, False, None, []),
    (T('Text'), False, URL('hebrew', 'text', vars=dict(mr='m')), []),
    (T('Words'), False, URL('hebrew', 'words'), []),
    (T('Queries'), False, URL('hebrew', 'queries'), []),
    (T('Notes'), False, URL('hebrew', 'notes'), []),
    (SPAN(_title='SHEBANQ Wiki', _class='fa fa-info-circle fa-2x'), False, 'https://github.com/ETCBC/shebanq/wiki', []),
]

response.about = 'https://github.com/ETCBC/shebanq/wiki'

if "auth" in locals(): auth.wikimenu() 
