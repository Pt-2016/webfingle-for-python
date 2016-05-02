#!/usr/bin/env python
#encoding=utf-8

import os,sys,time,string,Queue
import re,codecs,socket,httplib
import threading

from datetime import datetime
from elasticsearch import Elasticsearch
from fin_climb import climb_url

queues_		= Queue.Queue()
threads_num	= 200

class Mythread(threading.Thread):
	def __init__(self,func):
		super(Mythread,self).__init__()
		self.func = func
	def run(self):
		self.func()

def pt_scan():
	while not queues_.empty():
		climb_t	= queues_.get()
		climb_url(climb_t)		
		queues_.task_done()	
	
if __name__ == '__main__':
	if len(sys.argv) == 1:
		print 'Usage:[%s] + list.txt' % sys.argv[0] 
		sys.exit()
	try:
		threads = []
		target	= sys.argv[1]
		
		line = codecs.open(target,'r')
		lin = line.readlines()
		line.close()
		lin_sum = lin.__len__()
		for m in lin:
			m = m.strip('\n\r')
			queues_.put(m)
		for mm in xrange(threads_num):
			thread = Mythread(pt_scan)
			thread.start()
			threads.append(thread)
		for thread in threads:
			thread.join()
	
		queues_.join()

	except Exception, e:
		raise Exception('Exception %s' % str(e))
