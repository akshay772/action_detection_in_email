from enron_parser import parse_email
from spacy.lang.en import English
# from nltk.tag import pos_tag
# from nltk.tokenize import word_tokenize

import sys
import spacy

# filepath = sys.argv[1]

# inputs a single sentence tokenized and pos tagged list
def get_actionable_item(sent_tokenized_tagged):
    # maintain a file and import common list action verbs
    # importing list of action words
    list_action_words = ["do", "list", "document", "send", "forward", "fix", "write", "open", "wait",
        "move", "visit", "make", "listen", "come", "spend", "submit", "build", "bring", "ask", "grab",
        "read", "give", "act", "visit", "think", "drop", "call", "schedule"]
    # EXCEPTIONS LIST HERE IMPORT BELOW
    # maintain a two word phrase that do not indicate action but are combination of verbs
    two_gram_discard_phrases = []
    # maintain a three word phrase that do not indicate action but are combination of verbs
    three_gram_discard_phrases = ["to do list"]
    result = []
    # applying a simple rule to get the verb and the next conjunction for searching action
    for index in range(len(sent_tokenized_tagged)):
        if sent_tokenized_tagged[index][1] == "VB" and sent_tokenized_tagged[index][0] in \
                list_action_words:
            # print(sent_tokenized_tagged[index][0])
            # check if prev word is present in dicarded phrases list
            two_gram = sent_tokenized_tagged[index - 1][0] + " " + sent_tokenized_tagged[index][0]
            three_gram = sent_tokenized_tagged[index - 1][0] + " " + sent_tokenized_tagged[index][0] + " " \
                         + sent_tokenized_tagged[index + 1][0]
            # print(two_gram)
            if two_gram in two_gram_discard_phrases or three_gram in three_gram_discard_phrases:
                print("exception phrase is found... skipping...")
            # Here we are looking for text like (finish, complete, done)
            else:
                who_will_perform = ""
                for prev_tag in sent_tokenized_tagged[:index][::-1]:
                    # print(prev_tag[0])
                    # move in back direciton to know the word on which action is being performed on
                    if prev_tag[1] == "PRP" or prev_tag[1] == "NNP" or prev_tag[1] == "PRP$":
                        who_will_perform = prev_tag[0]
                        break
                action = ""
                to_complete = ""
                for msg_index, token in enumerate(sent_tokenized_tagged[index:]):
                    # look for the actionable next to conditioned tag
                    if token[1] == "IN":
                        for time_index, time_lookup in enumerate(sent_tokenized_tagged[msg_index:], msg_index):
                            if time_lookup[1] == "NN":
                                to_complete = sent_tokenized_tagged[time_index - 1][0] + " " + \
                                              sent_tokenized_tagged[time_index][0]
                            if time_lookup[1] == "PRP":
                                break
                        break
                    else:
                        action = action + " " + token[0]
                result += [dict(tasked_on=who_will_perform, action=action, completed_by=to_complete)]
    # print(result)
    return result

def load_spacy_sentecizer_pos_tagger():
    # load english tokenizer, tagger, parser, NER and word vectors
    # create pipe for sentence tokenize
    nlp = English()
    # create pipe for pos tagging
    pos_tagger = spacy.load("en_core_web_sm")
    # Create the pipeline 'sentencizer' component
    # sentencizer = Sentencizer(punct_chars=[".", "!", "?"]) # default punct_chars are these no need to import
    sbd = nlp.create_pipe("sentencizer")
    # add the component to pipeline
    nlp.add_pipe(sbd)

    return nlp, pos_tagger
# remove stop words from sentences
# spacy_stopwords = spacy.lang.en.stop_words.STOP_WORDS

def load_data_dict(filepath, max_no_email):
    # get the count of actionable to nonactionable
    # return only if current body actionable count is present
    # read the ENRON data into dict
    data_filepath = filepath
    email_dict = parse_email(data_filepath, max_no_email)
    final = { "actionable":0, "nonactionable":0 }
    # run for each email sample
    for key, email in email_dict.items():
        final["actionable"] = 0
        final["nonactionable"] = 0
        # print( "\n\n\nEmail no to analyse : %s" % key )
        # print(key, type(key), email["body"][0]["sub_body"])
        text = email["body"][0]["sub_body"]
        # removing new lines introduced in body due to email writting
        text = text.replace("\n", "")
        # "nlp" Object is used to create documents with linguistic annotations
        nlp, pos_tagger = load_spacy_sentecizer_pos_tagger()
        doc = nlp( text )
        # create list of sentence tokens
        all_sents_token_tags = [ ]
        for sent in doc.sents:
            count = 0
            sent_token = [ ]
            text_tagging = pos_tagger( sent.orth_ )
            for token in text_tagging:
                sent_token.append( [ token.orth_, token.tag_ ] )
                count += 1
            sent_action = get_actionable_item(sent_token)
            # print("\treturned dictionary is : ", sent_action)
            for element in sent_action:
                # do something
                if element["action"]:
                    final["actionable"] += 1
                else:
                    final["nonactionable"] += 1

        # print email actionable or non-actionable
        if final["actionable"] >= 1:
            print("\n\Email is actionable, with action grabbed as : %s \tPrinting mail no ... %s" % (
                element["action"], key))
        else:
            print( "\nEmail is non-actionable : \tPrinting mail no ... %s" % key )

        # # adding one more loop to loop through emails for nesting action to get insights in forwarded mails
        # body_list = []
        # for key, value in email["body"].items():
        #     # run loop for only main body
        #     # for checking action in main body or can be forwarded with action to duplicate
        #     print("entering in key %s \t%s" % (key, type(value)))
        #     if value["sub_body"]:
        #         # copy the written code for single list to iterate with string here
        #         # hence each string's sentences will be classified to actionable or non-actionable
        #         body_list.append(value["sub_body"])


# load_data_dict()