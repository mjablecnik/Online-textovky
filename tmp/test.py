def _indent(content):
	indent = 0
	lines = content.split("\n")
	count = 0
	for line in lines:
		try:
			if line[0] == "\t" and (line.count("if") > 0 or line.count("for") > 0):
				indent = 0
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
	#print lines
	return "\n".join(lines)




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
		
from time import localtime, strftime
import urllib2, time

for i in range(10):
	start_time = time.time()
	#print "start:"+strftime("%f%f%f", localtime())
	page = urllib2.urlopen("http://pygora.localhost.cz/index")
	print "konec:"+str(time.time()-start_time)
