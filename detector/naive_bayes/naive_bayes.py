import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support
from nltk import word_tokenize

def prepare_dataset(path):
    df = pd.read_csv(path)
    df["text"] = df["text"].apply(lambda x: str(x))
    df["label"] = df["label"].apply(lambda x: int(x))

    return df

def create_word_list(X_train):
    word_list = []
    for index, row in X_train.iterrows():
        try:
            tokens = word_tokenize(row['text'])
        except TypeError:
            continue
        [word_list.append(token) for token in tokens]

    return word_list

def create_word_occ_dict(unique_word_list, word_list):
    smoothing = 1
    word_occ_dict = {unique_word: 0 for unique_word in unique_word_list}
    word_list_length = len(word_list)
    unique_list_length = len(unique_word_list)

    for word in unique_word_list:
        n_word_given_word_list = word_list.count(word)
        p_word_given_word_list = (n_word_given_word_list + smoothing) / \
                                 (word_list_length + smoothing * unique_list_length)

        word_occ_dict[word.lower()] = p_word_given_word_list

    return word_occ_dict

def naive_bayes(text, probability_antisemitic, probability_nonantisemitic, antisemitic_dict, non_antisemitic_dict):
    tokens = word_tokenize(text)

    p_message_is_antisemitic = probability_antisemitic
    p_message_is_notantisemitic = probability_nonantisemitic

    for word in tokens:
        if not word in antisemitic_dict:
            continue

        p_message_is_antisemitic *= antisemitic_dict.get(word)

    for word in tokens:
        if not word in non_antisemitic_dict:
            continue

        p_message_is_notantisemitic *= non_antisemitic_dict.get(word)

    if p_message_is_antisemitic > p_message_is_notantisemitic:
        return 1
    elif p_message_is_antisemitic < p_message_is_notantisemitic:
        return 0
    else:
        return 3

def get_metrics(y_true,y_pred):
    return {"f1_score": f1_score(y_true,y_pred,average="micro"),
            "accuracy": accuracy_score(y_true,y_pred),
            "confusion_matrix": confusion_matrix(y_true,y_pred),
            "prec_rec_fscore": precision_recall_fscore_support(y_true,y_pred)
    }

def main():
    train = prepare_dataset("../data_without_slur_keywords_train.csv")
    test = prepare_dataset("../data_without_slur_keywords_test.csv")

    unique_word_list =list(dict.fromkeys(create_word_list(train)))

    antisemitic_word_list = create_word_list(train[train.label == 1])
    non_antisemitic_word_list = create_word_list(train[train.label == 0])

    antisemitic_dict = create_word_occ_dict(unique_word_list, antisemitic_word_list)
    non_antisemitic_dict = create_word_occ_dict(unique_word_list, non_antisemitic_word_list)

    probability_antisemitic = train['label'].value_counts(normalize=True)[1]
    probability_nonantisemitic = train['label'].value_counts(normalize=True)[0]

    test["predicted"] = test["text"].apply(naive_bayes,args=(probability_antisemitic, probability_nonantisemitic, antisemitic_dict, non_antisemitic_dict))

    y_pred = test["predicted"]
    y_true = test["label"]

    metrics = get_metrics(y_true,y_pred)
    print(metrics)

main()
