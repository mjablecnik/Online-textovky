#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
from time import localtime, strftime

def GetDatetime():
	return strftime("%Y-%m-%d %H:%M:%S", localtime())


DATABASE = {"server":"localhost",
			"user":"root",
			"password":"b5huha57",
			"database":"online_textovky"
			}

db = MySQLdb.connect(DATABASE["server"],DATABASE["user"],DATABASE["password"],DATABASE["database"])
cursor = db.cursor(MySQLdb.cursors.DictCursor)

sql = "select * from users;"

cursor.execute(sql)
users = cursor.fetchall()
datetime = GetDatetime()

for user in users:
	if str(user["last_chat_activity"])[:-2] != datetime[:-2]:
		sql = "update users set chat_online=0 where id=%s;" % user["id"]
		cursor.execute(sql)
		print user["id"]
		
db.commit()
db.close()
