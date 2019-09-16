from enron_parser import parse_email
from spacy.lang.en import English

# load english tokenizer, tagger, parser, NER and word vectors
# create pip for sentence tokenize
nlp = English()
# Create the pipeline 'sentencizer' component
# sentencizer = Sentencizer(punct_chars=[".", "!", "?"]) # default punct_chars are these no need to import
sbd = nlp.create_pipe("sentencizer")
# add the component to pipeline
nlp.add_pipe(sbd)

# read the ENRON data into dict
data_filepath = "./data/chunk.csv"
email_dict = parse_email(data_filepath)

# run for each email sample
# adding one more loop to loop through emails
body_list = []
for key, value in email_dict[14]["body"].items():
    print("entering in key %s \t%s" % (key, type(value)))
    if value["sub_body"]:
        # copy the written code for single list to iterate with string here
        # hence each string's sentences will be classified to actionable or non-actionable
        body_list.append(value["sub_body"])

# this is the code to be added to the loop above
# "nlp" Object is used to create documents with linguistic annotations
doc = nlp(body_list[0])

# create list of sentence tokens
sents_list = []
for sent in doc.sents:
	sents_list.append(sent.text)
print(sents_list)
