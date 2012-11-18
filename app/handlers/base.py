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
The BaseHandler
"""

from google.appengine.api import users
from webapp2 import RequestHandler, cached_property
from webapp2_extras import sessions

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"


class BaseHandler(RequestHandler):
    class __User(object):
        """
        A User instance just reflects the authentification status of the
        current *user* that sent the request. An instance of User should
        be attached to handler.user when authentification is needed.
        """
        def __init__(self, handler):
            user = users.get_current_user()
            if user:
                self.active = True
                self.id = user.user_id()
                self.nickname = user.nickname()
                self.email = user.email()
                self.name = "%s <%s>" % (self.nickname, self.email)
                self.admin = users.is_current_user_admin()
                self.logout = users.create_logout_url(handler.request.uri)
            else:
                self.active = False
                self.login = users.create_login_url(handler.request.uri)
    # Allows User to be called more attribute like:
    # self.User() instead of self.__User(self)
    User = lambda self: self.__User(self)

    def write(self, r):
        self.response.write(r)

    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    @cached_property
    def session(self):
        # Returns a session using the default cookie key.
        return self.session_store.get_session()

    def get_flashes(self, *args, **kwargs):
        return self.session.get_flashes(*args, **kwargs)

    def add_flash(self, title, msg="", level=""):
        level = "alert-" + level if level else ""
        return self.session.add_flash((title, msg), level)

    def __init__(self, request, response):
        self.initialize(request, response)
        self.user = self.User()
