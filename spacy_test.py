from enron_parser import parse_email
from spacy.lang.en import English
# from nltk.tag import pos_tag
# from nltk.tokenize import word_tokenize

import sys
import spacy

filepath = sys.argv[1]

# inputs a single sentence tokenized and pos tagged list
def get_actionable_item(sent_tokenized_tagged):
    # importing list of action words
    list_action_words = ["do", "list", "document"]
    list_discard_phrases = ["to do"]
    result = []
    # applying a simple rule to get the verb and the next conjunction for searching action
    for index in range(len(sent_tokenized_tagged)):
        if sent_tokenized_tagged[index][1] == "VB" and sent_tokenized_tagged[index][0] in \
                list_action_words:
            print(sent_tokenized_tagged[index][0])
            # check if prev word is present in dicarded phrases list
            two_gram = sent_tokenized_tagged[index - 1][0] + " " + sent_tokenized_tagged[index][0]
            print(two_gram)
            if two_gram in list_discard_phrases:
                print("exception phrase is found... skipping...")
            # Here we are looking for text like (finish, complete, done)
            else:
                who_will_perform = ""
                for prev_tag in sent_tokenized_tagged[:index][::-1]:
                    # print(prev_tag[0])
                    # move in back direciton to know the word on which action is being performed on
                    if prev_tag[1] == "PRP" or prev_tag[1] == "NNP":
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

def load_data_dict():
    # get the count of actionable to nonactionable
    # return only if current body actionable count is present
    final = {"actionable" : 0, "nonactionable" : 0}
    # read the ENRON data into dict
    data_filepath = filepath
    email_dict = parse_email(data_filepath)

    # run for each email sample
    for key, email in email_dict.items():
        print(key, type(key), email["body"])
        # adding one more loop to loop through emails
        body_list = []
        for key, value in email_dict[key]["body"].items():
            # run loop for only main body or if empty check next sub_body
            # for checking action in main body or can be forwarded with action to duplicate
            print("entering in key %s \t%s" % (key, type(value)))
    #         if value["sub_body"]:
    #             # copy the written code for single list to iterate with string here
    #             # hence each string's sentences will be classified to actionable or non-actionable
    #             body_list.append(value["sub_body"])
    #
    #
    #
    # # this is the code to be added to the loop above
    # # "nlp" Object is used to create documents with linguistic annotations
    # text = email_dict[14]["body"][1]["sub_body"]
    # # text = text.lower()
    # # removing new lines introduced in body due to email writting
    # text = text.replace("\n", "")
    # nlp, pos_tagger = load_spacy_sentecizer_pos_tagger()
    # doc = nlp(text)
    #
    # # create list of sentence tokens
    # all_sents_token_tags = []
    # for sent in doc.sents:
    #     count = 0
    #     sent_token = []
    #     # print(type(sent.orth_))
    #     text_tagging = pos_tagger(sent.orth_)
    #     # sent_tags = pos_tag(word_tokenize(sent.orth_))
    #     # print(sent_tags)
    #     for token in text_tagging:
    #         sent_token.append([token.lemma_, token.tag_]) # sent_tags[count]) # for using nltk tagger
    #         count += 1
    #     all_sents_token_tags.append(sent_token)
    # print(all_sents_token_tags[0], len(all_sents_token_tags))
    # # call sentence to see if action is present
    # print(get_actionable_item(all_sents_token_tags[0]))


load_data_dict()