import csv
from sklearn.model_selection import train_test_split
from transformers import DistilBertTokenizerFast

def create_test_train(file_name):
    """
    Read Texts and labels from created csv file and split in train and test set
    :param file_name: path to the csv source file
    :return: train and test sets
    """
    with open(file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        texts, labels = [], []

        for row in reader:

            texts.append(row["text"])
            labels.append(int(row["label"]))

    return train_test_split(texts, labels, test_size=.2)


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
