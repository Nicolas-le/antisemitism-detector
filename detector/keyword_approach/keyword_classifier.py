import pandas as pd
from nltk import word_tokenize
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support

def get_dataframe(path):
    df= pd.read_csv(path)
    df["text"] = df["text"].apply(lambda x: str(x))
    df["label"] = df["label"].apply(lambda x: int(x))

    return df

def classify_text(text):
    tokens = word_tokenize(text)

    # if there are slurs, immediately classified as antisem
    if any([True for token in tokens if token in keywords.keyword.values]):
        return True
    else:
        return False


def get_metrics(y_true,y_pred):
    return {"f1_score": f1_score(y_true,y_pred),
            "accuracy": accuracy_score(y_true,y_pred),
            "confusion_matrix": confusion_matrix(y_true,y_pred),
            "prec_rec_fscore": precision_recall_fscore_support(y_true,y_pred)
    }

def main():
    test = get_dataframe("../data_test.csv")

    test["predicted"] = test["text"].apply(classify_text)

    y_pred = test["predicted"]
    y_true = test["label"]


    metrics = get_metrics(y_true,y_pred)
    print(metrics)

keywords = pd.read_csv("keywords.csv")
main()

