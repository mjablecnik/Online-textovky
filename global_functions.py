#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cgi, os.path, re
from time import localtime, strftime
import hashlib, binascii, MySQLdb
from config import *


def GetDatetime():
	return strftime("%Y-%m-%d %H:%M:%S", localtime())

def GetTime():
	time = strftime("%H:%M:%S", localtime())
	if time[0]=="0":
		return time[1:]
	else:
		return time

def GetFile(file):
	f = open(file, "r")
	view = f.read()
	f.close()
	return view

def GetHash(password, datetime):
	salt = datetime+"*mllkeúor.-§ǘ*"
	h = hashlib.new('sha1')
	h.update(password+salt)
	return h.hexdigest()

def IsValidEmail(email):
	return re.match(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b', str(email)) != None
	
def EscapeHtmlSpecialChars(string):
	return cgi.escape(string, True).replace("'","&apos;")	
