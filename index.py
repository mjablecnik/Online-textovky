#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mod_python import apache, psp, Session, util
import MySQLdb
import os.path
from config import *
import pages as page
from global_functions import *
from database import Database
from website import Website



##########################################################


		
class Brandbook(Website):
	def __init__(self, req):
		super(Brandbook,self).__init__(req)
		self.session.set_timeout(60*60*15)
	
	def style(self):
		file = self.req.uri#.split("/")[-1:][0]
		return GetFile(HOME+file)

	def script(self):
		file = self.req.uri#.split("/")[-1:][0]
		return GetFile(HOME+file)
		
	def handler(self):
		pagebuffer = None
		"""Other files (img, js, etc...)"""
		if (self.req.uri[-4:] == '.css'):
			pagebuffer = self.style()
		elif (self.req.uri[-3:] == '.js'):
			pagebuffer = self.script()
		elif (self.req.filename.split("/")[-2] == 'images'):
			self.req.content_type = "image/gif"
			self.req.sendfile(HOME+req.uri)

		elif not self.session.has_key(SESSION_USER):
			self.session[SESSION_USER] = "Anonym"
			self.session.save()
			login = page.Login(self)
			login.show()
			pagebuffer = str(login)
		else:
			if(self.session[SESSION_USER] == "Anonym"):
				if (self.is_uri(Route.registration)):
					pagebuffer = str(page.Registration(self, Route.registration))
				elif (self.is_uri(Route.login) or self.req.uri == "/"):
					pagebuffer = str(page.Login(self, Route.login))
				else:
					login = page.Login(self)
					login.show()
					pagebuffer = str(login)
			else:

				if (self.is_uri(Route.index) or self.req.uri == '/' or self.req.uri == ''):
					pagebuffer = str(page.Index(self, Route.index))
				elif (self.is_uri(Route.chat)):
					pagebuffer = str(page.Chat(self, Route.chat))
				elif (self.is_uri(Route.members)):
					pagebuffer = str(page.Members(self, Route.members))
				elif (self.is_uri(Route.logout)):
					pagebuffer = str(page.Logout(self, Route.logout))
				elif (self.is_uri(Route.blog)):
					pagebuffer = str(page.Blog(self, Route.blog))
				
				else:
					pagebuffer = str("404")
		

		if(pagebuffer != None):
			self.req.write(pagebuffer)
		else:
			self.req.write("Stala se neočekávaná chyba, která se neměla nikdy stát.")
			
		return(apache.OK)

def handler(req):
	page = Brandbook(req)
	return page.handler()

