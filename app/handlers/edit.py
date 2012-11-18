# !/usr/bin/env python
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
Edit Handler
"""

from base import BaseHandler
from views import edit_tpl as tpl
from models import *

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"


class Handler(BaseHandler):
    def get(self, name):
        if not self.user.active:
            return self.redirect(self.user.login)
        if not name:
            return self.redirect("/_edit/FrontPage")
        page = get_page(name)
        if page is None:
            return self.write(tpl.render(page_name=name, user=self.user, edit_data=""))
        edit = get_edit(page, self.request.get('edit', default_value=None))
        self.write(tpl.render(page_name=name, user=self.user, edit_data=edit.data))

    def post(self, name):
        if not self.user.active:
            return self.redirect(self.user.login)
        if not name:
            name = "FrontPage"
        if not self.request.get("data", default_value=None):
            return self.redirect("?")
        page = add_page(name)
        edit = add_edit(page, self.user, self.request.get("data", default_value=None))
        self.redirect("/"+page.name)


