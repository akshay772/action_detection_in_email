# action_detection_in_email
A heuristics-based linguistic model for detecting actionable items from the email. A rule-based model to classify sentences to actionable sentence and non-actionable sentence.
* Learns common grammer rules to catch action/transition verbs in the mail and prints if ENRON
 dataset mails are actionable or non-actionable.
 * If mail is found actionable, it grabs the action part of the mail.

##### Requiremments : 
* To install dependencies run : `pip install -r requirements.txt`
    * Spacy is using  "en_core_web_sm" model so download it manually by running `python -m spacy download
     en_core_web_sm` in separate bash.

### How to run the module
* Download the dataset [here](https://www.kaggle.com/wcukierski/enron-email-dataset). 
* To run to classify a sentence : `python3 main.py "Sentence to classify"`
* Simple run to classify emails in ENRON dataset :  `python3main.py /Path/to/data/file/ number_1 number_2
 number_3` 
    * number_1 : Maximum no of chunks to run (to prevent system running out of memory)
    * number_2 : Chunk size to take for processing
    * number_3 : No of email to predict in each chunk

### Needs for improvement
* Increase the no of verb action words to increase the rule based classification.
* Add 2-gram and 3-gram words to boot the accuracy of model.
* Importing NLTK wordnet model to fetch and add synonyms of transition verbss
