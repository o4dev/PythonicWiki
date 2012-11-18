#!/usr/bin/env coffee
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

window.getEditor = ->
  baseUrl = "http://ajaxorg.github.com/ace-builds/textarea/src/"
  load = window.__ace_loader__ = (path, module, callback) ->
    head = document.getElementsByTagName("head")[0]
    s = document.createElement("script")
    s.src = baseUrl + path
    head.appendChild s
    s.onload = ->
      window.__ace_shadowed__.require [module], callback

  load "ace-bookmarklet.js", "ace/ext/textarea", ->
    ace = window.__ace_shadowed__
    ace.options =
      mode: "text"
      theme: "Monokai"
      gutter: "true"
      fontSize: "16px"
      softWrap: "off"
      showPrintMargin: "false"
      useSoftTabs: "true"
      showInvisibles: "false"

    Event = ace.require("ace/lib/event")
    area = document.getElementById("editor")
    if area
      ace.transformTextarea area, load