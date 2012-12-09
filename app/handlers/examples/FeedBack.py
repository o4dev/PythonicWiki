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
FeedBack example
"""

from handlers.base import BaseHandler
from google.appengine.api import channel
from views import feedback_tpl as tpl
from models import add_feedback


__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"

chan_name = "chat"

class obj(object):
    pass

page = obj()
page.name = "Feedback"
page.data = "<h1 style='width:100%;text-align:center;'>Thank you for your feedback ! :)</h1>"

page2 = obj()
page2.name = "Feedback"
page2.data = """
<h1>Give us some feedback on our wiki!</h1>
<form action="/_examples/Feedback" method="post">
    <table>
        <tr>
            <td style="vertical-align: top;"><lable>Message</lable></td>
            <td><textarea style="width: 700px; height: 500px;"name="data"></textarea></td>
        <tr>
    </table>
    <input type="submit">
</form>
"""

class Handler(BaseHandler):
    def get(self):
        if self.request.cookies.get('done'):
            return self.write(tpl.render(page=page, user=self.user, edit=page))
        self.write(tpl.render(page=page2, user=self.user, edit=page2))
    def post(self):
        if not self.request.cookies.get('done'):
            self.store_feed_back()
    def store_feed_back(self):
        ip = self.request.remote_addr
        data = self.request.get("data")
        add_feedback(ip, data)
        self.finalize()
    def finalize(self):
        self.response.set_cookie('done', '1')
        self.redirect('/_examples/Feedback')

