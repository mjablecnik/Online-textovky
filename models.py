#!/usr/bin/env python
# -*- coding: utf-8 -*-

from mod_python import apache
from database import Database

class User():
	TABLE = "users"
	id = "id"
	nick = "nick"
	email = "email"
	password_hash = "password_hash"
	created = "created"
	name = "name"
	surname = "surname"
	chat_online = "chat_online"
	last_chat_activity = "last_chat_activity"
	
	@staticmethod
	def get_id(db, user_email):
		user = db.select_one((User.id,), User.TABLE, where={User.email:user_email})
		return user[User.id]
		
	@staticmethod
	def get_nick(dbi, user_id):
		db=Database()
		db.select_columns((User.nick,))
		db.from_tables(User.TABLE)
		db.set_where({User.id:user_id})
		db.set_limit(1)
		db.execute_query()
		nick = db.fetchall()[0][User.nick]
		db.close()
		return nick

	@staticmethod
	def is_online(user_id):
		db = Database()
		db.select_columns((User.chat_online,))
		db.from_tables(User.TABLE)
		db.set_where({User.id:user_id})
		db.execute_query()
		user = db.fetchone()
		db.close()
		return user[User.chat_online]
		
	@staticmethod
	def get_columns():
		return (User.id, User.nick, User.email, User.password_hash, User.created, User.name, User.surname)
		
class Profile():
	TABLE = "profiles"
	user_id = "user_id"
	last_change = "last_change"
	user_profile = "user_profile"
	web = "web"
	job = "job"
	doing = "doing"
	story = "story"
	
	@staticmethod
	def get_columns():
		return (Profile.user_id, Profile.last_change, Profile.user_profile, Profile.web, Profile.job, Profile.doing, Profile.story)
		
class Message():
	TABLE = "chat_messages"
	user_id = "user_id"
	created = "created"
	message = "message"
	@staticmethod
	def get_columns():
		return (Message.user_id, Message.created, Message.message)
		
class WallMessage():
	TABLE = "wall_messages"
	id = "id"
	user_id = "user_id"
	created = "created"
	message = "message"
	@staticmethod
	def get_columns():
		return (WallMessage.id, WallMessage.user_id, WallMessage.created, WallMessage.message)

class WallComment():
	TABLE = "wall_comments"
	id = "id"
	wall_message_id = "wall_message_id"
	user_id = "user_id"
	created = "created"
	message = "message"
	@staticmethod
	def get_columns():
		return (WallMessage.id, WallMessage.user_id, WallMessage.created, WallMessage.message)
		
class OnlineUser():
	TABLE = "online_users"
	user_id = "user_id"
	@staticmethod
	def get_columns():
		return (OnlineUser.user_id, )

	@staticmethod
	def is_online(user_id):
		db = Database()
		db.select_columns((User.id,))
		db.from_tables(User.TABLE)
		db.execute_query()
		users = db.fetchall()
		db.close()
		
		for user in users:
			if user[User.id]==user_id:
				return True

		return False


