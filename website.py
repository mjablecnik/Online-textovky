#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mod_python import Session
from global_functions import *
from config import *
from models import *
from time import time
import os

class Website(object):
	def __init__(self, req):
		self.req = req
		self.session = Session.Session(req)
		self.flashmessage = ""
		
	def is_uri(self, uri):
		return (self.req.uri[:len(uri)] == uri)	
	
	def _indent(self, content):
		indent = 1
		lines = content.split("\n")
		count = 0
		for line in lines:
			try:
				if line.count("end") > 0:
					indent = 0
				elif line[0] == "\t" and (line.count("if") > 0 or line.count("for") > 0 or line.count("else") > 0):
					indent = 1
					for i in range(10):
						if line[i] == "\t":
							indent += 1
						else:
							break
				elif line[:7] == "content":
					lines[count] = "\t"*indent+line
				count += 1
			except Exception, ex:
				count += 1
				continue
				
		return "\n".join(lines)

	def _parse_template(self, template_name, model):
		start_time = time()
		content = self._get_template(template_name)
		indent = 0
		
		content = content.replace("<%=", '"""\ncontent+=model["') 
		content = content.replace("=%>", '"]\ncontent+="""')
		content = content.replace("<%", '"""\n') 
		content = content.replace("%>", '\ncontent+="""')
		content = content.replace("=>", ')\ncontent+="""') 
		content = content.replace("<=", '"""\ncontent+=str(')
		
		content = self._indent(content)
		#name =  str(time()-start_time)+".tmp"
		name =  "test.tmp"
		filepath = os.path.join(HOME, "tmp", name)
		f = open(filepath , "w")
		f.write('# -*- coding: utf-8 -*-\ncontent="""'+content+'\n"""\n')
		f.close()
		
		file = open(filepath , "r")
		exec file
		file.close()
		#os.system("rm "+filepath)
		return content
	
	def _get_partial_view(self, file, model):
		content = GetFile(os.path.join(HOME, "templates", file))
		for key, value in model.iteritems():
			content = content.replace("<%="+key+"=%>", value)
		return content

		
	def _get_template(self, file):
		return GetFile(os.path.join(HOME, "templates", file))



class Page(Website):
	def __init__(self, page):
		self.req = page.req
		self.session = page.session
		self.flashmessage = page.flashmessage
		self.log = ""
		self.response = ""
	
	def show(self, template_name, content_model={}, layout_model={}):
		try:
			content = self._parse_template(template_name, {"flashmessage":self.flashmessage})
			menu_selected = {"index_selected":"", 
								"blog_selected":"",
								"games_selected":"",
								"support_selected":"",
								"chat_selected":"",
								"profile_selected":"",
								"content":content
							}
			menu_selected.update(layout_model)
			self.response = self._parse_template(LAYOUT, menu_selected)
		except:
			self.response = "404"
	
	def show_part(self, template_name):
		self.response = self._parse_template(template_name, {"flashmessage":self.flashmessage})
	
	
	def __str__(self):
		if(self.log != ""):
			return self.log
		elif(self.response != ""):
			return self.response
		return ""
		
