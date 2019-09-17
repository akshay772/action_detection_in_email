import logging
# import sys
# import email
# import json
import pandas as pd

from email.parser import Parser
from os import path, listdir

def parse_email( pathname, max_no_email=15, orig=True ):
    all_mail = { }
    if path.isdir( pathname ):
        print( pathname )
        for child in listdir( pathname ):
            # only parse visible files
            if child[ 0 ] != ".":
                parse_email( path.join( pathname, child ), False )
    else:
        print( "file is ", pathname )
        df = pd.read_csv( pathname )

        count = 1
        for text in df.message:
            try:
                mail_contents = { }
                # print( "present count is %s" % count )
                if count == max_no_email + 1:
                    break
                message = Parser().parsestr( text )
                mail_contents[ "to" ] = message[ "to" ]
                mail_contents[ "from" ] = message[ "from" ]
                mail_contents[ "subject" ] = message[ "subject" ]
                mail_contents[ "cc" ] = message[ "cc" ]
                mail_contents[ "bcc" ] = message[ "bcc" ]

                # parse for mail body and convert to paragraphs
                # body structure from data is either just the body or the forwarded message
                body_text = message.get_payload()
                if "--- Forwarded" in body_text:
                    nested_body = { }
                    # use the flag to find original message in nested_body
                    original_flag = False
                    next_forward_flag = False
                    last_original = False
                    original_count = body_text.count( "-Original Message" ) + 1
                    # get forwarded msg body
                    for forward_count in range( body_text.count( "--- Forwarded" ) + original_count ):
                        # print( "\n\nforward count is : %s" % forward_count )
                        # take care of base case where msg is only forwarded or grabbing the base
                        mail_contents_nested = { }
                        if forward_count == 0:
                            test = body_text.partition( "--- Forwarded" )
                            if test[ 0 ].upper().isupper():
                                # finding last endline occurance
                                # print( "main body found" )
                                mail_contents_nested[ "sub_body" ] = test[ 0 ][ :test[ 0 ].rfind( "\n" ) ]
                            else:
                                mail_contents_nested[ "sub_body" ] = ""
                                # print( "only fowarded no main body" )
                            mail_contents_nested[ "to" ] = ""
                            mail_contents_nested[ "cc" ] = ""
                            mail_contents_nested[ "subject" ] = ""

                        else:
                            if last_original is True:
                                if "From:" in body_text:
                                    # print( "From address found in original" )
                                    mail_contents_nested[ "from" ] = body_text[
                                    body_text.find( "From:" ) + len( "From:" ): body_text[ body_text.find(
                                        "From:" ) + len( "From:" ): ].find( "Sent:" ) + 4 ]
                                    body_text = body_text[
                                    body_text[ body_text.find( "From:" ) + len( "From:" ): ].find(
                                        "To:" ) + 4: ]
                                else:
                                    # print( "From not found in original" )
                                    mail_contents_nested[ "from" ] = ""
                                if "To:" in body_text:
                                    # print( "To address found in original" )
                                    mail_contents_nested[ "to" ] = body_text[
                                    body_text.find( "To:" ) + len( "To:" ):body_text[
                                                                           body_text.find( "To:" ) + len(
                                                                               "To:" ): ].find(
                                        "Subject:" ) + 3 ]
                                    body_text = body_text[
                                    body_text[ body_text.find( "To:" ) + len( "To:" ): ].find(
                                        "Subject:" ) + 3: ]
                                else:
                                    # print( "To not found in original" )
                                    mail_contents_nested[ "to" ] = ""
                                if "Subject:" in body_text:
                                    # print( "Subject is found in original" )
                                    mail_contents_nested[ "subject" ] = body_text[
                                    body_text.find( "Subject:" ) + len( "Subject:" ):body_text[
                                                                                     body_text.find(
                                                                                         "Subject:" ) +
                                                                                     len(
                                                                                         "Subject:" ):
                                                                                     ].find(
                                        "\n\n" ) + 10 ]
                                    body_text = body_text[
                                    body_text[ body_text.find( "Subject:" ) + len( "Subject:" ): ].find(
                                        "\n\n" ) + 10: ]
                                else:
                                    # print( "Subject not found in original" )
                                    mail_contents_nested[ "subject" ] = ""
                            if "To:" in body_text and last_original is False:
                                # print( "To address found" )
                                mail_contents_nested[ "to" ] = body_text[
                                body_text.find( "To:" ) + len( "To:" ):body_text[
                                                                       body_text.find( "To:" ) + len(
                                                                           "To:" ): ].find( "cc:" ) + 2 ]
                                body_text = body_text[
                                body_text[ body_text.find( "To:" ) + len( "To:" ): ].find( "cc:" ) + 3: ]
                            else:
                                if last_original is False:
                                    # print( "To address not found not original" )
                                    mail_contents_nested[ "to" ] = ""
                            if "cc:" in body_text and last_original is False:
                                # print( "CC: address found" )
                                mail_contents_nested[ "cc" ] = body_text[
                                body_text.find( "cc:" ) + len( "cc:" ):body_text[
                                                                       body_text.find( "cc:" ) + len(
                                                                           "cc:" ): ].find(
                                    "Subject:" ) + 2 ]
                                body_text = body_text[
                                body_text[ body_text.find( "cc:" ) + len( "cc:" ): ].find(
                                    "Subject:" ) + 2: ]
                            else:
                                if last_original is False:
                                    # print( "CC address not found not original" )
                                    mail_contents_nested[ "cc" ] = ""
                            if "Subject:" in body_text and last_original is False:
                                # print( "Subject: found" )
                                mail_contents_nested[ "subject" ] = body_text[
                                body_text.find( "Subject:" ) + len( "Subject:" ):body_text[
                                                                                 body_text.find(
                                                                                     "Subject:" ) + len(
                                                                                     "Subject:" ): ].find(
                                    "\n\n" ) + 10 ]
                                body_text = body_text[
                                body_text[ body_text.find( "Subject:" ) + len( "Subject:" ): ].find(
                                    "\n\n" ) + 10: ]
                            else:
                                if last_original is False:
                                    # print( "Subject address not found not original" )
                                    mail_contents_nested[ "subject" ] = ""
                            # print(
                            #     "\noriginal flag is : %s \t next forward flag is : %s \t last original flag is : %s" % (
                            #     original_flag, next_forward_flag, last_original) )

                            if next_forward_flag is True:
                                # print( "next forward flag found... getting current body..." )
                                test = body_text.partition( "--- Forwarded" )
                                if test[ 0 ].upper().isupper():
                                    # finding last endline occurance
                                    # print( "initial body found" )
                                    mail_contents_nested[ "sub_body" ] = test[ 0 ][
                                    :test[ 0 ].rfind( "\n" ) ]
                                else:
                                    mail_contents_nested[ "sub_body" ] = ""
                                    # print( "only fowarded no main body" )

                            if next_forward_flag is False and original_flag is True and last_original \
                                    is False:
                                # print( "next original flag found... getting current body body of "
                                #        "forwarded mail..." )
                                test = body_text.partition( "-Original Message" )
                                if test[ 0 ].upper().isupper():
                                    # finding last endline occurance
                                    # print( "initial body found" )
                                    mail_contents_nested[ "sub_body" ] = test[ 0 ][
                                    :test[ 0 ].rfind( "\n" ) ]
                                else:
                                    mail_contents_nested[ "sub_body" ] = ""
                                    # print( "only fowarded no main body" )

                            if last_original and original_flag:
                                if body_text.count( "-Original Message" ):
                                    # print("multiple original bodies present... extracting current one...")
                                    test = body_text.partition( "-Original Message" )
                                    if test[ 0 ].upper().isupper():
                                        # finding last endline occurance
                                        mail_contents_nested[ "sub_body" ] = test[ 0 ][
                                        :test[ 0 ].rfind( "\n" ) ]
                                else:
                                    # print( "reached last original body finally" )
                                    mail_contents_nested[ "sub_body" ] = body_text

                            if next_forward_flag is False and original_flag is False and last_original is False:
                                # print( "only body is there so add directly to sub body" )
                                mail_contents_nested[ "sub_body" ] = body_text

                            next_forward_flag = False
                            original_flag = False


                        # extract body and fill in dict
                        if body_text.count( "--- Forwarded" ):
                            # print(body_text)
                            # print( "moving to the next nested forwarded body" )
                            body_text = body_text[ body_text.find( "--- Forwarded" ): ]
                            body_text = body_text[ body_text.find( "To:" ): ]
                            # print(body_text)
                            if body_text.count( "--- Forwarded" ):
                                # print( "found next forward flag" )
                                next_forward_flag = True
                            if body_text.count( "-Original Message" ):
                                # print( "found original flag" )
                                original_flag = True

                        # write code for extracting original message
                        else:
                            if body_text.count( "-Original Message" ):
                                # print(
                                #     "last original flag found... moving to the nested original body..." )
                                body_text = body_text[ body_text.find( "---Original Message" ): ]
                                body_text = body_text[ body_text.find( "From:" ): ]
                                # print(body_text)
                                # print(body_text)
                                last_original = True
                                original_flag = True

                        nested_body[ forward_count ] = mail_contents_nested
                    mail_contents[ "body" ] = nested_body
                else:
                    mail_contents[ "body" ] = { 0 : { "sub_body" : message.get_payload(), "to" : "",
                        "cc" : "", "subject" : "" }}

                all_mail[ count ] = mail_contents
                # print( json.dumps( all_mail, indent=2 ) )
            except Exception as ex:
                print( ex )
                logging.error( "Failed to parse %s" % pathname )
                return None
            finally:
                count += 1

    return all_mail

# run and test email parser
# print(parse_email( sys.argv[ 1 ] ))


