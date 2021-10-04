from transformers import DistilBertTokenizerFast
import pandas as pd

def create_test_train(train_csv,test_csv):
    """
    Read Texts and labels from created csv file and split in train and test set
    :param file_name: path to the csv source file
    :return: train and test sets
    """

    train = pd.read_csv(train_csv)
    test = pd.read_csv(test_csv)

    train['text'] = train['text'].apply(lambda x: str(x))
    train['label'] = train["label"].apply(lambda x: int(x))

    train_texts = train["text"].tolist()
    train_labels = train["label"].tolist()

    test['text'] = test['text'].apply(lambda x: str(x))
    test['label'] = test["label"].apply(lambda x: int(x))

    test_texts = test["text"].tolist()
    test_labels = test["label"].tolist()

    return train_texts, test_texts, train_labels, test_labels


def tokenize_train_test(train_texts, test_texts):
    """
    Using DistilBertTokenizer to keep tokenizing in same the technology stack as the training.
    :param train_texts:
    :param test_texts:
    :return:
    """
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    test_encodings = tokenizer(test_texts, truncation=True, padding=True)

    return train_encodings, test_encodings

def date_time_to_string(datetime):
    return datetime.strftime("%d_%m_%Y_%H_%M_%S")
