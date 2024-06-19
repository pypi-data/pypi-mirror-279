# Author: Scott Woods <scott.18.ansar@gmail.com>
# MIT License
#
# Copyright (c) 2017-2023 Scott Woods
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
__docformat__ = 'restructuredtext'

import ansar.create as ar
from .socketry import *
from .transporting_if import ts

__all__ = [
	'connect',
	'listen',
	'stop_listen',
]

def create_sockets(root):
	ts.sockets = root.create(SocketSelect)
	ts.channel = root.select(SocketChannel)

def stop_sockets(root):
	ts.channel.send(ar.Stop(), root.address)
	root.select(ar.Completed)

ar.AddOn(create_sockets, stop_sockets)

#
#
def connect(self, requested_ipp, session=None, encrypted=False, self_checking=False):
	"""
	Initiates a network connection to the specified IP
	address and port number.

	:param self: async entity
	:type self: Point
	:param requested_ipp: host and port to connect to
	:type requested_ipp: HostPort
	:param session: object to create on successful connection
	:type session: CreateFrame
	:param encrypted: is the server encrypting
	:type encrypted: bool
	:param self_checking: enable periodic enquiry/ack to verify transport
	:type self_checking: bool
	"""
	ts.channel.send(ConnectStream(requested_ipp=requested_ipp, create_session=session, encrypted=encrypted, self_checking=self_checking), self.address)

#
#
def listen(self, requested_ipp, session=None, encrypted=False):
	"""
	Establishes a network presence at the specified IP
	address and port number.

	:param self: async entity
	:type self: Point
	:param requested_ipp: host and port to listen at
	:type requested_ipp: HostPort
	:param session: object to create on successful connection
	:type session: CreateFrame
	:param encrypted: is the client encrypting
	:type encrypted: bool
	"""
	ts.channel.send(ListenForStream(requested_ipp=requested_ipp, create_session=session, encrypted=encrypted), self.address)

#
#
def stop_listen(self, requested_ipp):
	ts.channel.send(StopListening(requested_ipp), self.address)
