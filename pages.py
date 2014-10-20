#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mod_python import apache, util
import os.path
from config import *
from models import *
from global_functions import *

from website import Page

class Index(Page):
	def __init__(self, page, root_uri=Route.index):
		super(Index,self).__init__(page)
		self.show("content.html", layout_model={"index_selected":"selected"})
	
class Blog(Page):
	def __init__(self, page, root_uri=Route.blog):
		super(Blog,self).__init__(page)
		self.show("blog.html", layout_model={"blog_selected":"selected"})

class Chat(Page):
	def __init__(self, page, root_uri=Route.chat):
		super(Chat,self).__init__(page)
		
		def parse_form():
			form = util.FieldStorage(self.req)
			self.message = form.getfirst("message")
			self.last_update = form.getfirst("last_update")
			
		def save_message():
			try:
				db = Database()
				user_id = self.session[SESSION_USER]
				model = {}
				model[Message.user_id] = user_id
				model[Message.created] = GetTime()
				model[Message.message] = self.message				
				
				#self.user_nick = User.get_nick(db, user_id)
				db.insert(model, Message.TABLE)
			
				db.close()
				return True
			except Exception, ex:
				return False
			
		def save_bot_message(message):
			try:
				db = Database()
				model = {}
				model[Message.user_id] = BOT_ID
				model[Message.created] = GetTime()
				model[Message.message] = message				
				
				db.insert(model, Message.TABLE)
			
				db.close()
				return True
			except Exception, ex:
				return False
		def load_last_messages(num=15, in_time=None):
			def get_messages():
				db = Database()
				if in_time != None:
					where = {User.id:self.session[SESSION_USER]}
					db.update({User.last_chat_activity:GetDatetime()}, User.TABLE, where)
					db.set_where({Message.created:in_time})
				else:
					user_id = self.session[SESSION_USER]
					if not User.is_online(user_id):
						db.update({User.chat_online:1}, User.TABLE, {User.id:user_id})
						nick = User.get_nick(db, user_id)
						save_bot_message("Uživatel %s se přihlásil do chatu." % nick)

				db.select_columns(Message.get_columns())
				db.from_tables(Message.TABLE)
				db.execute_query()
				messages = db.fetchall()
				db.close()
				return messages

			lines = ""
			messages = get_messages()[-num:]
			for message in messages:
				nick = User.get_nick(None, message[Message.user_id])
				lines += "<b>[%s] %s:</b> %s <br/>\n" % (message[Message.created], nick, message[Message.message])
					
			return lines
			
		def run():	
			if (self.req.uri == root_uri+"/send_post"):
				parse_form()
				if save_message():
					self.response += ""
				else:
					self.response += "[%s] Chyba: Někde se stala nečekaná chyba.<br/>\n" % GetTime()
			
			elif (self.req.uri == root_uri+"/send_update"):
				parse_form()
				time = self.last_update
				second = int(time[-2:])
				time = time[:-2] + str(second-1)
				self.response += load_last_messages(in_time=time)

			elif(self.req.uri == root_uri):
				self.lines = load_last_messages()
				self.show()
		run()

	def show(self):
		content = self._parse_template("chat.html", {"flashmessage":self.flashmessage, "messages":self.lines})
		menu_selected = {"index_selected":"", 
							"blog_selected":"",
							"games_selected":"",
							"support_selected":"",
							"chat_selected":"",
							"profile_selected":"",
							"content":content
						}
		menu_selected["chat_selected"] = "selected"
		self.response = self._parse_template(LAYOUT, menu_selected)
		
class Members(Page):
	def __init__(self, page, root_uri=Route.members):
		super(Members,self).__init__(page)
		db = Database()
		#self.model = db.join_select(User.get_columns(), (Profile.user_profile, Profile.job, Profile.doing), User.TABLE, Profile.TABLE, order_by=User.name)
		
		db.select_columns( (User.id, User.email, User.name, User.surname), (Profile.job, Profile.doing, Profile.user_profile) )
		db.from_tables(User.TABLE, Profile.TABLE, User.id, Profile.user_id)
		db.set_where({User.id:2}, symbol="!=")
		db.set_order(User.name, type=db.DESC)
		db.set_limit(20)
		
		db.execute_query()
		self.model = db.fetchall()
		db.close()
		self.response = db.get_sql()
		self.show("members.html")

class Registration(Page):
	def __init__(self, page, root_uri=Route.registration):
		super(Registration,self).__init__(page)
		
		def parse_form():
			form = util.FieldStorage(self.req)
			self.email = form.getfirst("email")
			self.pass1 = form.getfirst("pass1")
			self.pass2 = form.getfirst("pass2")
		
		def validate():
			if not IsValidEmail(self.email):
				self.flashmessage += "Špatně zadaný email.<br/>"
			if (self.pass1 == None or len(self.pass1) < 6):
				self.flashmessage += "Heslo musí být dlouhé alespoň 6 znaků.<br/>"
			if (self.pass1 != self.pass2):
				self.flashmessage += "Hesla se musí shodovat.<br/>"
		
		def save_user_and_redirect():
			datetime = GetDatetime()
			def get_usermodel():
				model = {}
				model[User.nick] = self.email.split("@")[0]
				model[User.email] = self.email
				model[User.created] = datetime
				model[User.password_hash] = GetHash(self.pass1, datetime)
				return model
			try:	
				db = Database()
				db.insert(get_usermodel(), User.TABLE)
				user_id = User.get_id(db, self.email)
				db.insert( {Profile.user_id:user_id, Profile.last_change:datetime, Profile.story:"Zde napište svůj příběh."} , Profile.TABLE)
				db.close()
			
				self.flashmessage += "Registrace proběhla úspěšně. Nyní se můžete přihlásit.<br/><br/>"
				login = Login(self)
				login.show()
				self.response = str(login)
			except Exception, ex:
				self.flashmessage += str(ex)+"<br/>Někde se stala nějaká neznámá chyba, <br/>kontaktujte admina: %s<br/><br/>" % ADMIN_EMAIL
				self.show()
		
		def run():
			if(self.req.uri == root_uri):
				self.show()
			elif(self.req.uri == root_uri+"_send"):
				parse_form()
				validate()
				if (self.flashmessage != ""):	
					self.show()
				else:
					save_user_and_redirect()
		run()
			
	def show(self):
		super(Registration,self).show("registration.html")
		
class Login(Page):
	def __init__(self, page, root_uri=Route.login):
		super(Login,self).__init__(page)
		self.user = None
		
		def parse_form():
			form = util.FieldStorage(self.req)
			self.email = form.getfirst("email")
			self.password = form.getfirst("password")
		
		def login():
			try:
				db = Database()
				columns = { User.id, User.email, User.password_hash, User.created }
				db.select_columns(columns)
				db.from_tables(User.TABLE)
				db.set_where({User.email:self.email})
				db.set_limit(1)
				db.execute_query()
				user = db.fetchall()[0]
				db.close()

				hash = GetHash(self.password, str(user[User.created]))
				if hash == user[User.password_hash]:
					self.user = user
					return True
				
				return False
			except Exception, ex:
				self.flashmessage += str(ex)
				return False
			
		def try_login():
			if login():
				self.session[SESSION_USER] = self.user[User.id]
				self.session.save()
				Redirect.index(self.req)
			else:
				self.flashmessage += "Přihlášení proběhlo neúspěšně. Email nebo heslo není správně.<br/>"
				self.show()
		
		def run():
			if(self.req.uri == root_uri+"_send"):
				parse_form()
				try_login()
				
			elif(self.req.uri == root_uri):
				self.show()

		run()
		
	def show(self):
		super(Login,self).show("login.html")

class Logout(Page):
	def __init__(self, page, root_uri=Route.logout):
		super(Logout,self).__init__(page)
		self.session.delete()
		Redirect.login(self.req)	
