# to read ENRON data in chunks and print if the mail is actionable or non actionable
# print the action if mail found actionable
import os
import sys
import pandas as pd

from spacy_test import load_data_dict

# read csv chunks
filepath = sys.argv[1]
if not os.path.isfile(filepath):
    print("Inputting a sentence")
else:
    print("Path to data file : ", filepath)
    no_chunks = int(sys.argv[2])
    print("Maximum no of chunks to process : ", no_chunks)
    chunk_size = int(sys.argv[3])
    print("Chunk size to take for processing : ", chunk_size)
    max_no_email = int(sys.argv[4])
    print("No of email to be process in each data file chunk : ", max_no_email)

if os.path.isfile(filepath):
    count = 0
    for chunk in pd.read_csv(filepath, chunksize=chunk_size):
        if count > no_chunks:
            break
        if not os.path.exists("./data"):
            os.makedirs("./data")
        chunk.to_csv( "./data/chunk.csv", index=False )
        print("\nChunk saved...")
        # process(chunk)
        print("chunk no ... %s\n processing \t Wait for results...\n\n" % (count+1))
        # call spacy_test.py module to get actionable mails
        load_data_dict(filepath, max_no_email)
        # lastly remove the saved chunk to process next chunks
        print("Chunk deleted\n")
        os.remove("./data/chunk.csv")
        count += 1
else:
    # doing processing for string
    # call spacy_test.py module to get actionable mails
    load_data_dict( filepath, 1 )