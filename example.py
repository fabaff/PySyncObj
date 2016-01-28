#!/usr/bin/env python

import sys
import time
from syncobj import SyncObj, replicated


class TestObj(SyncObj):

	def __init__(self, selfNodeAddr, otherNodeAddrs):
		super(TestObj, self).__init__(selfNodeAddr, otherNodeAddrs)
		self.__counter = 0

	@replicated
	def incCounter(self):
		self.__counter += 1

	@replicated
	def addValue(self, value):
		self.__counter += value

	def getCounter(self):
		return self.__counter


if __name__ == '__main__':
	if len(sys.argv) < 3:
		print 'Usage: %s self_port partner1_port partner2_port ...'
		sys.exit(-1)

	port = int(sys.argv[1])
	partners = []
	for i in xrange(2, len(sys.argv)):
		partners.append('localhost:%d' % int(sys.argv[i]))

	o = TestObj('localhost:%d' % port, partners)
	n = 0
	while True:
		time.sleep(0.005)
		if o._getLeader() is None:
			continue
		if n < 2000:
			o.addValue(10)
		n += 1
		if n % 200 == 0:
			print 'Counter value:', o.getCounter(), o._getLeader(), o._getRaftLogSize()
