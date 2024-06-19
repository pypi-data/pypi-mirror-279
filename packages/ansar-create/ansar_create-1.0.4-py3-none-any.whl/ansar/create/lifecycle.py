# MIT License
#
# Copyright (c) 2017 Scott Woods
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

"""Standard Ansar messages.

These are either generated from within Ansar - and then expected by the
application in related scenarios. Or they are used internally by Ansar
and may be used in the wider application. Ansar async objects will
exhibit common patterns of behaviour.
"""
__docformat__ = 'restructuredtext'

import re
import ansar.encode as ar

__all__ = [
	'Start',
	'Completed',
	'Stop',
	'Pause',
	'Resume',
	'Aborted',
	'TimedOut',
	'AWOL',
	'Overloaded',
	'OutOfService',
	'Nothing',
	'Ready',
	'NotReady',
	'Ping',
	'Enquiry',
	'Ack',
	'Nak',
	'Anything',
]


# Fundamental birth and death of
# an async object
class Start(object):
	"""First message received by every async machine, from creator to child."""
	pass

class Completed(object):
	"""Last message sent, from child to creator.

	:param value: return value for an async object
	:type value: any
	"""
	def __init__(self, value=None):
		self.value = value

# Basic external controls
class Stop(object):
	"""Initiate teardown in the receiving object."""
	pass

class Pause(object):
	"""Suspend operation in the receiving object."""
	pass

class Resume(object):
	"""Resume operation in the receiving object."""
	pass

# Additions to the base Faulted.
#
def timed_out(timer):
	if timer is None:
		return 'ding'

	t = ar.tof(timer)
	return f'"{t}" exceeded'

def latest_further(lf):
	latest, further = lf
	if latest is None:
		if further is None:
			return '(unspecified)'
		f = ar.show_fault(further)
		return f'({f})'
	v = ar.show_fault(latest)

	if further is None:
		return f'{v}'
	f = ar.show_fault(further)

	return f'{v} ({f})'

def service_update(nlf):
	if len(nlf) == 0:
		return 'internal', '(zero services)'

	absent = {f'{k}': latest_further(lf) for k, lf in nlf.items()}
	text = ar.name_text(absent)
	return absent, text

class Aborted(ar.Faulted):
	def __init__(self, error_code=None, exit_code=None):
		ar.Faulted.__init__(self, 'aborted', 'user or software interrupt', error_code=error_code, exit_code=exit_code)

class TimedOut(ar.Faulted):
	def __init__(self, timer=None):
		text = timed_out(timer)
		ar.Faulted.__init__(self, 'timed out', text)
		self.timer = timer

class Exhausted(ar.Faulted):
	def __init__(self, final_straw=None, attempts=None, started=None, ended=None, seconds=None):
		self.final_straw = final_straw
		self.attempts = attempts
		self.started = started
		self.ended = ended
		self.seconds = seconds

		error_code = None
		exit_code = None
		if final_straw and isinstance(final_straw, ar.Faulted):
			error_code = final_straw.error_code
			exit_code = error_code

		if started is not None:
			if ended is None:
				self.ended = ar.world_now()
			if seconds is None:
				d = self.ended - self.started
				self.seconds = d.total_seconds()

		if final_straw is not None:
			t = ar.tof(final_straw)
			condition = f'final attempt "{t}"'
		else:
			condition = 'exhausted'
		
		if attempts is None or started is None:
			explanation = None
		else:
			s = ar.world_to_text(self.started)
			explanation = f'{attempts} attempts over {self.seconds} seconds starting at {s}'

		ar.Faulted.__init__(self, condition, explanation, error_code=error_code, exit_code=exit_code)

class AWOL(ar.Faulted):
	def __init__(self, error_code=None, exit_code=None, **nvf):
		unavailable, text = service_update(nvf)
		ar.Faulted.__init__(self, 'temporarily unavailable', text, error_code=error_code, exit_code=exit_code)
		self.unavailable = unavailable

class Overloaded(ar.Faulted):
	def __init__(self, error_code=None, exit_code=None, **nvf):
		overloaded, text = service_update(nvf)
		ar.Faulted.__init__(self, 'temporarily overloaded', text, error_code=error_code, exit_code=exit_code)
		self.overloaded = overloaded

class OutOfService(ar.Faulted):
	def __init__(self, error_code=None, exit_code=None, **nvf):
		out_of_service, text = service_update(nvf)
		ar.Faulted.__init__(self, 'out of service', text, error_code=error_code, exit_code=exit_code)
		self.out_of_service = out_of_service

TIMED_OUT_SCHEMA = {
	'timer': ar.Any,
}

EXHAUSTED_SCHEMA = {
	'final_straw': ar.Any(),
	'attempts': ar.Integer8(),
	'started': ar.WorldTime(),
	'ended': ar.WorldTime(),
	'seconds': ar.Float8(),
}

AWOL_SCHEMA = {
	'absent': ar.MapOf(ar.Unicode(), ar.Unicode()),
}

OVERLOADED_SCHEMA = {
	'overloaded': ar.MapOf(ar.Unicode(), ar.Unicode()),
}

OUT_OF_SERVICE_SCHEMA = {
	'out_of_service': ar.MapOf(ar.Unicode(), ar.Unicode()),
}


TIMED_OUT_SCHEMA.update(ar.FAULTED_SCHEMA)
EXHAUSTED_SCHEMA.update(ar.FAULTED_SCHEMA)
AWOL_SCHEMA.update(ar.FAULTED_SCHEMA)
OVERLOADED_SCHEMA.update(ar.FAULTED_SCHEMA)
OUT_OF_SERVICE_SCHEMA.update(ar.FAULTED_SCHEMA)

ar.bind(Start, copy_before_sending=False)
ar.bind(Completed, object_schema={'value': ar.Any()}, copy_before_sending=False)
ar.bind(Stop, copy_before_sending=False)
ar.bind(Pause, copy_before_sending=False)
ar.bind(Resume, copy_before_sending=False)

ar.bind(Aborted, object_schema=ar.FAULTED_SCHEMA, copy_before_sending=False)

ar.bind(TimedOut, object_schema=TIMED_OUT_SCHEMA, copy_before_sending=False)
ar.bind(Exhausted, object_schema=EXHAUSTED_SCHEMA, copy_before_sending=False)
ar.bind(AWOL, object_schema=AWOL_SCHEMA, copy_before_sending=False)
ar.bind(Overloaded, object_schema=OVERLOADED_SCHEMA, copy_before_sending=False)
ar.bind(OutOfService, object_schema=OUT_OF_SERVICE_SCHEMA, copy_before_sending=False)

#
#
class Nothing(object):
	"""A positive null."""
	pass

class Ready(object):
	"""Report a positive state."""
	pass

class NotReady(object):
	"""Report a positive state."""
	pass

# Most basic sync and/or status check.
#
class Ping(object):
	"""Test for reachability."""
	pass

class Enquiry(object):
	"""Prompt an action from receiver."""
	pass

class Ack(object):
	"""Report in the positive."""
	pass

class Nak(object):
	"""Report in the negative."""
	pass

ar.bind(Nothing, copy_before_sending=False)
ar.bind(Ready, copy_before_sending=False)
ar.bind(NotReady, copy_before_sending=False)
ar.bind(Ping, copy_before_sending=False)
ar.bind(Enquiry, copy_before_sending=False)
ar.bind(Ack, copy_before_sending=False)
ar.bind(Nak, copy_before_sending=False)

#
class Anything(object):
	def __init__(self, thing=None):
		self.thing = thing

ANYTHING_SCHEMA = {
	'thing': ar.Any,
}

ar.bind(Anything, object_schema=ANYTHING_SCHEMA)
