#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import types
from global_functions import *
from config import *

class Database():
	def __init__(self):
		self.db = MySQLdb.connect(DATABASE["server"],DATABASE["user"],DATABASE["password"],DATABASE["database"])
		self.cursor = self.db.cursor(MySQLdb.cursors.DictCursor)
		self.sql = ""
		self.select = ""
		self.from_table = ""
		self.where = ""
		self.order = ""
		self.limit = ""
		self.ASC = "ASC"
		self.DESC = "DESC"
		
	def fetchall(self):
		return self.cursor.fetchallDict()

	def fetchone(self):
		return self.cursor.fetchallDict()[0]
	
	def _check_model(self, model):
		for key, value in model.iteritems():
			model[key] = EscapeHtmlSpecialChars(str(value))
		return model
	
	def insert(self, model, table):
		try:
			model = self._check_model(model)
			keys = ", ".join(model.keys())
			values = "%s, " * len(model.values())
			values = values[:-2]
			
			self.sql = "INSERT INTO %s (%s) VALUES (%s);" % (table, keys, values)
			self.cursor.execute(self.sql, tuple(model.values()))
			self.db.commit()
			return True
		except:
			return False	

	def update(self, model, table, where={}):
		set_values = ""
		for key, value in model.iteritems():
			set_values += "%s='%s', " % (key, EscapeHtmlSpecialChars(str(value)))
		set_values = set_values[:-2]

		self.set_where(where)
		self.sql = "UPDATE %s SET %s %s;" % (table, set_values, self.where)
		self.execute_sql()
		self.db.commit()
		self.clear()
		return True
	
	
	def select_columns(self, col1, col2=None):
		if col2 == None:
			self.select = "SELECT T1.%s " % ( ", T1.".join(col1) )
		else:
			self.select = "SELECT T1.%s, T2.%s " % ( ", T1.".join(col1), ", T2.".join(col2) )
	
	def from_tables(self, table1, table2="", col1="", col2=""):
		if (table2 == "" or col1=="" or col2==""):
			self.from_table = "FROM %s T1 " % table1
		else:
			self.from_table = """FROM %s T1 INNER JOIN %s T2 ON T1.%s = T2.%s """ % (table1, table2, col1, col2)
	
	def set_where(self, model, symbol="="):
		if model != {}:
			if self.where == "":
				self.where = "WHERE"
			else:
				self.where += "AND"
			
			value = EscapeHtmlSpecialChars(str(model.values()[0]))
			self.where += " %s %s '%s' " % (model.keys()[0], symbol, value)
	
	def set_where_text(self, data):
		if self.where == "":
			self.where = " WHERE "
		else:
			self.where += " AND "
		self.where += EscapeHtmlSpecialChars(str(data))
	
	def set_order(self, by, type="ASC"):
		if self.order == "":
			self.order = "ORDER BY %s %s" % (by, type)
		else:
			self.order += " AND %s %s" % (by, type)
			
	def set_limit(self, limit):
		self.limit = " LIMIT %s" % str(limit)
			
	def execute_query(self, sql=""):
		if sql == "":
			self.build_sql()
			self.execute_sql()
		else:
			self.execute_sql()
	
	def execute_sql(self, sql=""):
		self.cursor.execute(self.sql)
	
	def build_sql(self):
		self.sql = self.select + self.from_table + self.where + self.order + self.limit + ";"
	
	def set_sql(self, sql):
		self.sql = sql
	
	def get_sql(self):
		return self.sql
	
	def clear(self):
		self.select = ""
		self.from_table = ""
		self.where = ""
		self.order = ""
		self.limit = ""
	
	def close(self):
		self.db.close()
