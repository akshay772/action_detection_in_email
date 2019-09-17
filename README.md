# action_detection_in_email
A heuristics-based linguistic model for detecting actionable items from the email. A rule-based model to classify sentences to actionable sentence and non-actionable sentence.
* Learns common grammer rules to catch action/transition verbs in the mail and prints if ENRON
 dataset mails are actionable or non-actionable.
 * If mail is found actionable, it grabs the action part of the mail.
### How to run the module
* Download the dataset [here](https://www.kaggle.com/wcukierski/enron-email-dataset). 
* Simple run the command `python main.py /Path/to/data/file/ number_1 number_2 number_3` 
    * number_1 : Maximum no of chunks to run (to prevent system running out of memory)
    * number_2 : Chunk size to take for processing
    * number_3 : No of email to predict in each chunk

### Needs for improvement
* Increase the no of verb action words to increase the rule based classification.
* Add 2-gram and 3-gram words to boot the accuracy of model.
