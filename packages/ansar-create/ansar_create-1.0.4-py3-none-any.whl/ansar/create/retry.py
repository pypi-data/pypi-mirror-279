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

"""Support for the concept of attempts and retries.

There is an object that tries to complete a task. If it fails, subsequent
attempts may be appropriate. A clear and robust implementation of this concept
is hugely useful in the context of networking. There is also a need for
refinement - "blunt force" retries can quickly create its own problems.
"""
__docformat__ = 'restructuredtext'

import random
import ansar.encode as ar

__all__ = [
	'RetryIntervals',
	'intervals_only',
	'smart_intervals',
]

#
#
random.seed()

# All times are subject to the accuracy of the internal timer service, e.g. 0.25s
# The randomized value should be a multiple of the timer accuracy.
# Step 1 should be at least twice of randomized
# The value of first steps should increase.
# Regular steps should be bigger than the last first step.
# All attributes except first_steps, can be set to None.
# There must be at least first steps or regular steps or both.
# Regular steps without a truncated value is an expression of forever.
# The defaults are based on the retry strategy frop SIP.
# Randomization is loosely based on exponential backoff.

class RetryIntervals(object):
	def __init__(self, first_steps=None, regular_steps=None, step_limit=None, randomized=None, truncated=None):
		self.first_steps = first_steps or ar.default_vector()
		self.regular_steps = regular_steps
		self.step_limit = step_limit
		self.randomized = randomized
		self.truncated = truncated

RETRY_INTERVALS_SCHEMA = {
	'first_steps': ar.VectorOf(ar.Float8()),
	'regular_steps': ar.Float8(),
	'step_limit': ar.Integer8(),
	'randomized': ar.Float8(),
	'truncated': ar.Float8(),
}

ar.bind(RetryIntervals, object_schema=RETRY_INTERVALS_SCHEMA)

# Coroutine to generate the sequence
# implied by first_steps and regular_steps.
def intervals_only(retry):
	for i in retry.first_steps:
		yield i
	if retry.regular_steps is None:
		return
	# For ever perhaps capped by
	# limit.
	while True:
		yield retry.regular_steps

# Wrap it in another coroutine that implements
# truncations and randomization of the underlying
# sequence.
def smart_intervals(retry):
	limit = retry.step_limit
	randomized = retry.randomized
	truncated = retry.truncated
	def cooked(r):
		if randomized is None:
			return r
		if truncated is None:
			t = r
		else:
			t = r * truncated
		m = int(t / retry.randomized) + 1
		s = random.randrange(0, m)
		c = s * retry.randomized
		return r + c

	if limit is None:
		for r in intervals_only(retry):
			yield cooked(r)
		return

	for _, r in zip(range(limit), intervals_only(retry)):
		yield cooked(r)
