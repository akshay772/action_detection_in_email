import sys
import email
import pandas as pd

from os import path, listdir

def parse_email(pathname, orig=True):
	if path.isdir(pathname):
		print(pathname)
		emails = []
		for child in listdir(pathname):
			# only parse visible files
			if child[0] != ".":
				parse_email(path.join(pathname, child), False)
				
	else:
		print("file is ", pathname)
		df = pd.read_csv(pathname)
		text = df.message[12]
		# print(text)
		try:
			try:
				message = email.message_from_string(text)
				count = 0
				for part in message.walk():
					print("part : %s \n\n\n %s" %(count+1, part))
			except AttributeError:
				print("something")
				# message = text
		except AttributeError:
			logging.error( "Failed to parse %s" % pathname )
			return None
			
	return "Success"

parse_email(sys.argv[1])