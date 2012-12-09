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

log = null

window.chatClient = (token, uid) ->
	window.uid = uid
	window.token = token
	channel = new goog.appengine.Channel(token)
	window.channel = channel
	socket = channel.open()
	window.socket = socket
	socket.onmessage = onMessage
	socket.onopen = onOpen
	socket.onerror = onError
	socket.onclose = onClose
	log = $("#log")
	$("#send").click(sendMessage)
	$('#chat input').keypress (e) ->
		if e.which == 13
			sendMessage()
	return socket

sendMessage = ->
	msg = $("#chat input").val()
	$("#chat input").val("")
	console.log ("SEND:" + msg)
	xhr = new XMLHttpRequest()
	xhr.open("POST", "?msg=#{msg}&uid=#{window.uid}", true)
	xhr.send()


onMessage = (msg) ->
	msg = msg.data
	console.log ("NEW:" + msg)
	log.append(msg)

onOpen = ->
	console.log("OPEN: connection open")

onClose = ->
	console.log("CLOSE: connection closed")

onError = (error) ->
	console.log("ERROR" + error)