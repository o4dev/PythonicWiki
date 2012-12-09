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
WebSocket example
"""

from handlers.base import BaseHandler
from google.appengine.api import channel
from google.appengine.api import memcache
from views import websockets_tpl as tpl, channel_tpl as tpl2
import logging
import re
import uuid

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"


PREFIX = "chat-"

def gen_key():
    uid = uuid.uuid4()
    return uid.hex

def get_keys(chan):
    keys = memcache.get(PREFIX+chan)
    if keys is not None:
        return keys
    memcache.set(PREFIX+chan, [])
    return []

def get_key(chan):
    key = gen_key()
    keys = get_keys(chan)
    if key in keys:
        return get_key(chan)
    keys.append(key)
    memcache.set(PREFIX+chan, keys)
    return key



class Handler(BaseHandler):
    def get(self, chan=None, *args):
        if not chan or chan == "/":
            return self.write(tpl2.render())
        key = get_key(chan)
        token = channel.create_channel(key)
        self.write(tpl.render(token=token, name=chan, uid=key))

    def post(self, chan):
        msg = self.request.get("msg")
        uid = self.request.get("uid")
        if not msg or not uid:
            return
        keys = get_keys(chan)
        user = keys.index(uid)
        msg = "<li>%s ---> <span>%s</span>" % (user, msg)
        for key in get_keys(chan):
            channel.send_message(key, msg)
