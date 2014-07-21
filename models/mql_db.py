#!/usr/bin/env python
#-*- coding:utf-8 -*-

# Copyright 2014 DANS-KNAW
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# # Fake imports and web2py variables. See also: __init__.py
# This code only serves to satisfy the editor. It is never executed.
if 0:
    from . import *
    # End of fake imports to satisfy the editor.
    #

from gluon.validators import Validator, is_empty
from select_or_add_option_widget import SELECT_OR_ADD_OPTION


class IS_MQL_QUERY(Validator):

    def __call__(self, value):
        value, empty = is_empty(value, empty_regex=None)
        if empty:
            return value, 'Enter a query'

        words = ['select', 'all', 'objects', 'where']
        missing_words = []
        l_value = value.lower()
        pos = 0
        for word in words:
            pos = l_value.find(word, pos, len(l_value))
            if pos < 0:
                missing_words.append(word)

        if len(missing_words) == len(words):
            value = 'SELECT ALL OBJECTS WHERE\n' + value

        if 0 < len(missing_words) < len(words):
            return value, 'The query is invalid. Missing or misplaced key words: ' + str(missing_words)

        return value, None


db.define_table('project',
                Field('name', 'string'),
                Field('website', 'string', requires=IS_URL()),
                format=lambda r: r.name or 'unknown',  # Necessary for SELECT_OR_ADD_OPTION widget
                )

db.define_table('organization',
                Field('name', 'string'),
                Field('website', 'string', requires=IS_URL()),
                format=lambda r: r.name or 'unknown',  # Necessary for SELECT_OR_ADD_OPTION widget
                )

# Define read-only signature
signature = db.Table(db, 'auth_signature',
                     Field('is_active', 'boolean', default=True,
                           writable=False, readable=False),
                     Field('created_on', 'datetime', default=request.now,
                           writable=False, readable=True),
                     Field('created_by', auth.settings.table_user,
                           default=auth.user_id,
                           writable=False, readable=True),
                     Field('modified_on', 'datetime',
                           update=request.now, default=request.now,
                           writable=False, readable=True),
                     Field('modified_by', auth.settings.table_user,
                           default=auth.user_id, update=auth.user_id,
                           writable=False, readable=True)
                     )

# Define the query table
db.define_table("queries",
                Field('name', 'string', requires=IS_NOT_EMPTY(error_message='Enter a name for the query')),
                Field('description', 'text', requires=IS_NOT_EMPTY(error_message='Enter the description of the query')),
                Field('mql', 'text', requires=IS_MQL_QUERY()),
                Field('project', 'reference project', requires=IS_IN_DB(db, db.project.id, '%(name)s'), widget=SELECT_OR_ADD_OPTION("project", controller='select_or_add_option_widget').widget),
                Field('organization', 'reference organization', requires=IS_IN_DB(db, db.organization.id, '%(name)s'), widget=SELECT_OR_ADD_OPTION("organization", controller='select_or_add_option_widget').widget),

                signature,
                format=lambda r: r.name or r.id,)

db.define_table("monadsets",
                Field('query_id', 'reference queries'),
                Field('first_m', 'integer'),
                Field('last_m', 'integer'))