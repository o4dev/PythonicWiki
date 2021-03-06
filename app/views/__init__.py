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
The Jinja template's __init__
"""

import os
import jinja2
from utils import fix_pagename, strip_tags

__author__ = "Luke Southam <luke@devthe.com>"
__copyright__ = "Copyright 2012, DEVTHE.COM LIMITED"
__license__ = "The BSD 3-Clause License"
__status__ = "Development"

DEBUG = True if os.environ.get(
    'SERVER_SOFTWARE', '').startswith('Development') else False


if False: #DEBUG:
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                       os.path.join(
                                       os.path.dirname(__file__), '.')),
                        extensions=['pyjade.ext.jinja.PyJadeExtension'], cache_size=0)
else:
    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(
                                       os.path.join(
                                       os.path.dirname(__file__), '.')),
                        extensions=['pyjade.ext.jinja.PyJadeExtension'])

jinja_env.globals['fix_pagename'] = fix_pagename
jinja_env.globals['strip_tags'] = strip_tags
jinja_env.globals['str'] = str

websockets_tpl = jinja_env.get_template('websockets.jade')
channel_tpl = jinja_env.get_template('websockets_channel.jade')
feedback_tpl = jinja_env.get_template('feedback.jade')
view_tpl = jinja_env.get_template('view.jade')
edit_tpl = jinja_env.get_template('edit.jade')
history_tpl = jinja_env.get_template('history.jade')
view_404_tpl = jinja_env.get_template('view.404.jade')