#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os.path 
from mod_python import util

HOME = os.path.dirname(os.path.abspath(__file__))
LAYOUT = "layout.html"
DOMAIN = "http://textovky.localhost.cz"
ADMIN_EMAIL = "admin@brandbook.cz"
SESSION_USER = "user_id"
BOT_ID = 36

DATABASE = {"server":"localhost",
			"user":"root",
			"password":"b5huha57",
			"database":"online_textovky"
			}

class Route():
	index = "/index"
	registration = "/registrace"
	login = "/prihlaseni"
	chat = "/chat"
	profile = "/profil"
	my_wall = "/moje-zed"
	public_wall = "/verejna-zed"
	members = "/clenove"
	logout = "/odhlaseni"
	blog = "/blog"
	support = "/podpora"
	games = "hry"

class Redirect():
	@staticmethod
	def registration(req):
		util.redirect(req, DOMAIN+Route.registration)
		
	@staticmethod
	def index(req):
		util.redirect(req, DOMAIN+Route.index)	
		
	@staticmethod
	def login(req):
		util.redirect(req, DOMAIN+Route.login)
	
	@staticmethod
	def chat(req):
		util.redirect(req, DOMAIN+Route.chat)
	
