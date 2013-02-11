#!/usr/bin/env python
###################
# Internet whois client
#
# Copyright Jean-Michel Philippe (c) 2007
#   <http://philipjm.free.fr/blog/>
# Original code from Fredrik Lundh <effbot@telia.com> posted on:
#   http://mail.python.org/pipermail/python-list/2000-March/028122.html
#
# This is open source software released under the GPL license.
# The full text of this license is found in the file 'LICENSE',
# included with this source code package.
###################

"""
Internet whois client module.

Typical use:

 >>> Whois = whois.WhoisConsumer('194.109.137.218')
 >>> whois.WhoisRequest(Whois, whois.WhoisServer)
 <whois._whois.WhoisRequest at -0x4a62ce74>
 >>> whois.asyncore.loop()
 >>> print Whois.text
 [...]
"""

###################
# importations
import asyncore
import socket

###################
class WhoisRequest(asyncore.dispatcher_with_send):
	"""
	Simple Internet whois requestor.
	"""
	
	def __init__(self, consumer, host, port=43):
		"""
		Queries a whois Internet service.
		
		>>> WhoisRequest(consumer, host)
		
		Input:
			- consumer	= a WhoisConsumer object instance
			- host		= the whois server host IP string
		"""
		asyncore.dispatcher_with_send.__init__(self)
	
		self.consumer = consumer
		self.query = consumer.host
	
		self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connect((host, port))
	
	def handle_connect(self):
		self.send(self.query + "\r\n")
	
	def handle_expt(self):
		self.close() # connection failed, shutdown
		self.consumer.abort()
	
	def handle_read(self):
		# get data from server
		self.consumer.feed(self.recv(2048))
	
	def handle_close(self):
		self.close()
		self.consumer.close()

###################
class WhoisConsumer:
	def __init__(self, host):
		"""
		Defines a consumer IP.
		
		>>> consumer = WhoisConsumer(host)
		
		Input:
			- host		= host IP string
		"""
		self.text = ""
		self.host = host
		self.status = 'init'
	
	def feed(self, text):
		self.status = 'answer'
		self.text = self.text + text
	
	def abort(self):
		self.status = 'abort'
	
	def close(self):
		self.status = 'ok'

###############
# try it out
if __name__ == '__main__':
	consumerList = []
	for host in ("69.72.153.218", "209.67.219.74", "196.200.67.140"):
		consumerList.append( WhoisConsumer(host) )
		request = WhoisRequest(consumerList[-1], host, "whois.arin.net")
	
	# loop returns when all requests have been processed
	asyncore.loop()
	import re
	for consumer in consumerList:
		Country = re.findall('[Cc]ountry:\s+(\w+)', consumer.text)
		if len(Country):
			Country = Country[0]
		else:
			Country = '???'
		print consumer.host, "from", Country
