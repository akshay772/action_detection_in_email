import logging
import sys
import email
import pandas as pd

from email.parser import Parser
from os import path, listdir

def parse_email(pathname, orig=True):
	all_mail = {}
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
		
		count = 1
		for text in df.message:
			email_body = []
			try:
				mail_contents = {}
				print("present count is %s" % count)
				if count == 73:
					break
				if count == 72:
					message = Parser().parsestr(text)
					mail_contents["to"] = message["to"]
					mail_contents["from"] = message["from"]
					mail_contents["subject"] = message["subject"]
					mail_contents["cc"] = message["cc"]
					mail_contents["bcc"] = message["bcc"]
					# print(mail_contents)
					
					# parse for mail body and convert to paragraphs
					# body structure from data is either just the body or the forwarded message
					body_text = message.get_payload()
					if "--- Forwarded" in body_text:
						nested_body = {}
						# use the flag to find original message in nested_body
						original_flag = False
						next_forward_flag = False
						last_original = False
						# print(body_text.partition("--- Forwarded"), body_text.count("--- Forwarded"))
						# get forwarded msg body
						for forward_count in range(body_text.count("--- Forwarded") + 2):
							print("\n\nforward count is : %s" % forward_count)
							# take care of base case where msg is only forwarded or grabbing the base
							mail_contents_nested = {}
							if forward_count == 0:
								test = body_text.partition( "--- Forwarded" )
								if test[0].upper().isupper():
									# finding last endline occurance
									print("main body found")
									mail_contents_nested["sub_body"] = test[0][:test[0].rfind("\n")]
								else:
									mail_contents_nested["sub_body"] = ""
									print("only fowarded no main body")
								mail_contents_nested["to"] = ""
								mail_contents_nested["cc"] = ""
								mail_contents_nested["subject"] = ""
							
							else:
								if "To:" in body_text:
									print( "To address found")
									mail_contents_nested["to"] = body_text[body_text.find("To:") + len(
											"To:"):body_text[body_text.find("To:") + len("To:"):].find(
											"cc:") + 2]
									body_text = body_text[body_text[body_text.find("To:") + len("To:"):].find(
											"cc:") + 3:]
								else:
									mail_contents_nested["to"] = ""
								if "cc:" in body_text:
									print( "CC: address found" )
									mail_contents_nested["cc"] = body_text[body_text.find("cc:") + len(
											"cc:"):body_text[body_text.find("cc:") + len("cc:"):].find(
											"Subject:") + 2]
									body_text = body_text[body_text[body_text.find("cc:") + len("cc:"):].find(
											"Subject:") + 2:]
								else:
									mail_contents_nested["cc"] = ""
								if "Subject:" in body_text:
									print( "Subject: found" )
									mail_contents_nested["subject"] = body_text[body_text.find("Subject:") + len(
											"Subject:"):body_text[body_text.find("Subject:") + len(
											"Subject:"):].find("\n\n\n") + 10]
									body_text = body_text[body_text[body_text.find("Subject:") + len(
											"Subject:"):].find("\n\n\n") + 10:]
								else:
									mail_contents_nested["subject"] = ""
								# nested_text = Parser().parsestr(body_text)
								print( "\noriginal flag is : %s \t next forward flag is : %s \t last "
								       "original flag is : %s" % (original_flag, next_forward_flag, last_original) )
								# print(body_text)
								# print(type(nested_text))
								if next_forward_flag is True and original_flag is True:
									print("next forward flag found... getting current body...")
									test = body_text.partition( "--- Forwarded" )
									if test[0].upper().isupper():
										# finding last endline occurance
										print( "initial body found" )
										mail_contents_nested["sub_body"] = test[0][:test[0].rfind( "\n" )]
									else:
										mail_contents_nested["sub_body"] = ""
										print( "only fowarded no main body" )
									next_forward_flag = False
									original_flag = False
									
								if next_forward_flag is False and original_flag is True and last_original \
										is False:
									print("next original flag found... getting current body body of "
									      "forwarded mail...")
									test = body_text.partition( "-Original Message" )
									# print(test[0].rfind( "\n" ))
									# print(test[0][970:984])
									if test[0].upper().isupper():
										# finding last endline occurance
										print( "initial body found" )
										mail_contents_nested["sub_body"] = test[0][:test[0].rfind( "\n" )]
									else:
										mail_contents_nested["sub_body"] = ""
										print( "only fowarded no main body" )
									next_forward_flag = True
									original_flag = False
									
									
								if last_original and original_flag:
									print("reached original body finally")
									mail_contents_nested["sub_body"] = body_text
								
								if next_forward_flag is False and original_flag is False and last_original \
										is False:
									print("only body is there so add directly to sub body")
									mail_contents_nested["sub_body"] = body_text
								
								next_forward_flag = False
									
							# extract body and fill in dict
							if body_text.count("--- Forwarded"):
								# if forward_count == 0:
								# 	print(body_text)
								print("moving to the next nested forwarded body")
								body_text = body_text[body_text.find( "--- Forwarded" ):]
								body_text = body_text[body_text.find( "To:" ):]
								# print(body_text.partition( "To:" ))
								# if forward_count == 0:
								# 	print(body_text)
								if body_text.count("--- Forwarded"):
									print("found next forward flag")
									next_forward_flag = True
								if body_text.count("-Original Message"):
									print("found original flag")
									original_flag = True
							
							# write code for extracting original message
							else:
								if body_text.count("-Original Message"):
									print("last original flag found... moving to the nested original body...")
									body_text = body_text[body_text.find("---Original Message"):]
									body_text = body_text[body_text.find("From:"):]
									# print(body_text)
									last_original = True
									original_flag = True
									
								
							nested_body[forward_count] = mail_contents_nested
							# print(nested_body)
							# print(nested_body)
							# print("body no : %s \n\n %s\n\n" % (forward_count, test))
						# print("body structure of email is : %s" % nested_body)
						mail_contents["body"] = nested_body
						print("do somehtings")
					else:
						mail_contents["body"] = {"1" : message.get_payload()}
					all_mail[count] = mail_contents
					print(all_mail)
			except Exception as ex:
				print(ex)
				logging.error( "Failed to parse %s" % pathname )
				return None
			finally:
				count += 1
				# print("current mail is : %s", all_mail)
				
	return "Success"

parse_email(sys.argv[1])