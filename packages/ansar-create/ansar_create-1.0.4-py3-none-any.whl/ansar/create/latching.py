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

import ansar.encode as ar

from .point import *
from .lifecycle import *
from .machine import *

__all__ = [
	'SwitchOver',
	'Reclaim',
	'Latch',
]

#
#
class SwitchOver(object):
	def __init__(self, address=None):
		self.address = address

SWITCH_OVER_SCHEMA = {
	'address': ar.Address(),
}

ar.bind(SwitchOver, object_schema=SWITCH_OVER_SCHEMA)

#
#
class Reclaim(object): pass

ar.bind(Reclaim, copy_before_sending=False)

#
#
SAVED_IN_LATCH = 32

class INITIAL: pass
class STANDBY: pass
class CARETAKER: pass

class Latch(Point, StateMachine):
	def __init__(self, key, default_address):
		Point.__init__(self)
		StateMachine.__init__(self, INITIAL)
		self.key = key
		self.default_address = default_address
		self.saved = ar.deque()
		self.session = None
		self.original = None
		self.alias = None		# Where this object sits and watches

def Latch_INITIAL_Start(self, message):
	self.original = self.address
	return STANDBY

def Latch_STANDBY_SwitchOver(self, message):
	session = message.address
	if session:
		self.alias = self.abdicate_to(session)
		self.session = session
	else:
		self.alias = self.abdicate_to(self.default_address)
		self.session = self.default_address

	for m, r in self.saved:
		self.forward(m, self.session, r)
	self.reply(Ack())
	return CARETAKER

def Latch_STANDBY_Stop(self, message):
	self.complete(Aborted())

def Latch_STANDBY_Unknown(self, message):
	s = (message, self.return_address)
	self.saved.append(s)
	len_saved = len(self.saved)
	if len_saved > SAVED_IN_LATCH:
		self.saved.popleft()
	return STANDBY

def Latch_CARETAKER_Unknown(self, message):
	self.forward(message, self.session, self.return_address)
	return CARETAKER

def Latch_CARETAKER_Reclaim(self, message):
	if self.alias:
		self.reclaim_original(self.original)
		self.alias = None
		self.saved = ar.deque()

	self.reply(Ack())
	return STANDBY

def Latch_CARETAKER_Stop(self, message):
	if self.alias:
		self.discard(self.alias)
	self.complete(Aborted())

LATCH_DISPATCH = {
	INITIAL: (
		(Start,), ()
	),
	STANDBY: (
		(SwitchOver, Stop, ar.Unknown), ()
	),
	CARETAKER: (
		(Reclaim, Stop, ar.Unknown), ()
	),
}

# FIDDLER BEWARE. VERY FRAGILE ASSIGNMENT OF THREADS.
# Having Latch and SubscriptionAgent on the same thread is
# a fix/patch/hack to prevent problem with message being
# in the queue at the time of an abdicate.
bind_statemachine(Latch, LATCH_DISPATCH, thread='subscribed')
