import pandas as pd

from spacy.lang.en import English
# from spacy.pipeline import Sentencizer

# load english tokenizer, tagger, parser, NER and word vectors
nlp = English()

filename = "./emails.csv"

# loading csv in chunks
chunks_size = 10
chunk =  pd.read_csv(filename, chunksize=chunks_size)
print(chunk.get_chunk(1)["message"])

text = """When learning data science, you shouldn't get discouraged!
Challenges and setbacks aren't failures, they're just part of the journey. You've got this!"""

# 'nlp' Object is used to create documents with linguistic annotations
my_doc = nlp(text)

# create word list of tokens
token_list = []
for token in my_doc:
	token_list.append(token)
# print(token_list)

# # Create the pipeline 'sentencizer' component
# sentencizer = Sentencizer(punct_chars=[".", "!", "?"]) # default punct_chars are these no need to import
sbd = nlp.create_pipe("sentencizer")

# add the component to pipeline
nlp.add_pipe(sbd)

# "nlp" Object is used to create documents with linguistic annotations
doc = nlp(text)

# create list of sentence tokens
sents_list = []
for sent in doc.sents:
	sents_list.append(sent.text)
# print(sents_list)

# use of stop
