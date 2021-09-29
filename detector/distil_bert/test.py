from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW, EvalPrediction
from transformers import pipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support
import pandas as pd
from sklearn.model_selection import train_test_split


def classifier():
    model_name = "./models/with_keywords/28_09_2021_19_34_44"
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    return classifier

antisem_classifier = classifier()

def prepare_dataset(path):
    dataset = pd.read_csv(path)
    return train_test_split(dataset,test_size=0.2,random_state=42)

def classify(sentence):

    """
    try:
        print(sentence)
    except UnicodeEncodeError:
        sentence = ""
    """

    classifcation = antisem_classifier(sentence[:512])[0]["label"]

    if classifcation == "LABEL_0":
        return 0
    else:
        return 1

def metrics(y_true,y_pred):
    return {"f1_score": f1_score(y_true,y_pred),
            "accuracy": accuracy_score(y_true,y_pred),
            "confusion_matrix": confusion_matrix(y_true,y_pred),
            "prec_rec_fscore": precision_recall_fscore_support(y_true,y_pred)

    }

def test():

    train, test = prepare_dataset("../data_train.csv")

    test['predicted'] = test['text'].apply(classify)
    y_pred = test["predicted"]
    y_true = test["label"]

    print(metrics(y_true,y_pred))


test()


