import re
from os import path, listdir
import sys
import json

# Precompiled patterns
msg_start_pattern = re.compile("\n\n", re.MULTILINE)
msg_end_pattern = re.compile("\n+.*\n\d+/\d+/\d+ \d+:\d+ [AP]M", re.MULTILINE)

feeds = []

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
		with open(pathname) as TextFile:
			text = TextFile.read().replace("\r", "")
			# print(text[:100], type(text))
			try:
			
	return "Success"

parse_email(sys.argv[1])