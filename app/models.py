#!/usr/bin/env python
#
# Copyright (c) 2012, Luke Southam <luke@devthe.com>
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# - Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# - Redistributions in binary form must reproduce the above copyright
#   notice, this list of conditions and the following disclaimer in
#   the documentation and/or other materials provided with the
#   distribution.
#
# - Neither the name of the DEVTHE.COM LIMITED nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND
# CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES,
# INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS
# BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
# EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
# TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
# ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF
# THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.
"""
The Database Model - WIKI
"""

import pickle
from google.appengine.ext.db import *
import json

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"

class Struct:
    def __init__(self, **entries): 
        self.__dict__.update(entries)

class ObjectProperty(TextProperty):
    def validate(self, value):
        return value

    def get_value_for_datastore(self, model_instance):
        result = super(ObjectProperty, self).get_value_for_datastore(model_instance)
        if not result.__class__.__name__ == "str":
            result = dict(result.__dict__)
            result = json.dumps(result)
        return Text(result)

    def make_value_from_datastore(self, value):
        value = json.loads(str(value))
        value = Struct(**value)
        

        return super(ObjectProperty, self).make_value_from_datastore(value)


class Page(Model):
    """
    The data model used for a wiki page. Mainly just used to
    reference edits.
    """
    name = StringProperty()
    datetime = DateTimeProperty(auto_now=True)


class Edit(Model):
    """
    The data Model used for a edit of a wiki page.
    """
    page = ReferenceProperty(Page, collection_name='edits')
    datetime = DateTimeProperty(auto_now_add=True)
    user = ObjectProperty()
    data = TextProperty()


def get_page(name):
    return Page.gql("WHERE name = :name", name=name).get()


def get_edits(page):
    return list(page.edits.order("datetime"))


def get_edit(page, number=-1):
    if number is None:
        number = -1
    try:
        return get_edits(page)[int(number)]
    except IndexError:
        return get_edits(page)[-1]


def delete_page(page):
    # deletes all edits of page
    for edit in get_edits(page):
        edit.delete()
    return page.delete()


def delete_edit(edit):
    return edit.delete()


def add_page(name):
    page = get_page(name)
    if page:
        return page
    page = Page()
    page.name = name
    page.put()
    return page

def add_edit(page, user, data):
    edit = Edit()
    edit.page = page
    edit.user = user
    edit.data = data
    edit.put()
    return edit
