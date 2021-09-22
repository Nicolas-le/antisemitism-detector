import pandas as pd
import re
from spacy.lang.en import English
from spacy.attrs import LOWER

sms_spam = pd.read_csv('../data_train.csv')

# split training and test set

# Randomize the dataset
data_randomized = sms_spam.sample(frac=1, random_state=1)

# Calculate index for split
training_test_index = round(len(data_randomized) * 0.8)

# Split into training and test sets
training_set = data_randomized[:training_test_index].reset_index(drop=True)
test_set = data_randomized[training_test_index:].reset_index(drop=True)


def create_word_list(messages):
    word_list = []
    for message in messages:
        # tokenize
        [word_list.append(token.text) for token in message]

    return word_list

unique_word_list = list(dict.fromkeys(create_word_list(training_set["text"])))

# create word lists containing all the appearing words for spam and ham messages
spam_word_list = create_word_list(training_set[training_set.Label == "antisemitic"]["text"])
ham_word_list = create_word_list(training_set[training_set.Label == "notantisemitic"]["text"])
unsure_word_list = create_word_list(training_set[training_set.Label == "unsure"]["text"])


def create_word_occ_dict(unique_word_list, word_list):
    smoothing = 1
    word_occ_dict = {unique_word: 0 for unique_word in unique_word_list}
    word_list_length = len(word_list)
    unique_list_length = len(unique_word_list)

    for word in unique_word_list:
        n_word_given_word_list = word_list.count(word)
        p_word_given_word_list = (n_word_given_word_list + smoothing) / (
                    word_list_length + smoothing * unique_list_length)

        word_occ_dict[word.lower()] = p_word_given_word_list

    return word_occ_dict