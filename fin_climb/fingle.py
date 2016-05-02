#!/usr/bin/env python
#encoding=utf-8

import os,sys,time,string,Queue
import re,codecs,socket,httplib
import threading

from datetime import datetime
from elasticsearch import Elasticsearch

E_time  = time.strftime('%Y-%m-%d',time.localtime(time.time()))
E_stat  = 999
E_server= 'unknown'
E_tit   = 'Exception Link!'

def es_insert(e_target,e_port,e_tit,e_pb,e_status,e_server,e_ip,e_time):
	try:
		tt_status = str(e_status)
		es = Elasticsearch('127.0.0.1:9200')
		#es.indices.create(index='test',ignore=400) 
		##can use "curl -XDELETE 'http://1.1.1.148:9200/webfingle'" delete webfingle index
		s1 = es.index(index='test_5_2',doc_type='web_type',id = e_ip,body={'t_target':e_target,'t_port':e_port,'t_title':e_tit,'t_pb':e_pb,'t_status':e_status,'t_servertype':e_server,'t_scantime':e_time})
		print 'Save ok!'
	except Exception, e:
		print '[Exception is]', e
		#exit(1)


def view_bar(everyline,line_sum):
	num = everyline
	sum = line_sum
	bar = "#"
	rate = float(num) / float(sum)
	rate_num = int(rate * 100)

	if rate >= 0.01 and rate <= 1.0:
		print '\r%3d%% :' %(rate_num),
		sys.stdout.flush()
	else:
		print '\r%3s%%:' % ('x')	

def handle_hd(head):
	for m in head:
		for n in m:
			if n == 'server':
				return m[1]
			else:
				pass

def handle_jump(head):
	for x in head:
		for y in x:
			if y == 'location':
				return x[1]
			else:
				pass

def handle_title(tt):
	if tt.__len__() == 0:
		return tt
	else:
		return tt[0][7:-8]

def handle_design(head):
	for h in head:
		for hh in h:
			if hh == 'x-powered-by':
				return h[1]
			else:
				pass

def climb_url(url_str):
	i = url_str
	if i.find(':') < 0:
		i_port  = '80'
		i_ip	= i
		try:
			con2    = httplib.HTTPConnection(i_ip,i_port,timeout = 3)
			con2.request("GET","/")
			st2     = con2.getresponse()
			stat    = st2.status
			heads   = st2.getheaders()
			hc      = st2.read()
			mssg    = st2.msg
			ti     	= re.findall('<title>.*</title>',hc)

			tit 	= handle_title(ti)
			server  = handle_hd(heads)
			powered_by	= handle_design(heads)			
			pb		= powered_by

			if stat == 302:
				jumpurl = handle_jump(heads)
				print pb
				es_insert(i,i_port,jumpurl,pb,stat,server,i_ip,E_time)
				print '\33[34m{0:<20}\33[31m|{1:<18}\33[35m|{2:^}\33[32m{3:<20}'.format(url_str,server,tit,jumpurl)
			elif stat == 404:
				print 'Ip is invalid'
			else:
				print pb
				print '\33[34m{0:<20}\33[31m|{1:<18}\33[35m|{2:^}'.format(url_str,server,tit)
				es_insert(i,i_port,tit,pb,stat,server,i_ip,E_time)
			
		except Exception, e:
			print '[Exception is]', e
			#exit(1)
			#pass
	else:
		i_ip, i_port = i.split(':')
		try:
			con2	= httplib.HTTPConnection(i_ip,i_port,timeout = 3)
			con2.request("GET","/")
			st2		= con2.getresponse()
			stat	= st2.status
			heads	= st2.getheaders()		
			hc  	= st2.read()
			mssg	= st2.msg
			ti	 	= re.findall('<title>.*</title>',hc)

			tit		= handle_title(ti)
			server 	= handle_hd(heads)				
	
			if stat == 302:
				jumpurl = handle_jump(heads)
				#es_insert(i,i_port,i_ip,stat,server,jumpurl,E_time)
				print '\33[34m{0:<20}\33[31m|{1:<18}\33[35m|{2:^}\33[32m{3:<20}'.format(url_str,server,tit,jumpurl)
			elif stat == 404:
				print 'Ip is invalid'
				#print '\33[34m{0:<20}\33[31m|{1:<18}\33[35m|{2:^}'.format(url_str,server,tit)
			else:
				print '\33[34m{0:<20}\33[31m|{1:<18}\33[35m|{2:^}'.format(url_str,server,tit)
				#es_insert(i,i_port,i_ip,stat,server,tit,E_time)					

		except Exception, e:
			print '[Exception is]', e
			#pass
