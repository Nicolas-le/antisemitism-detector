from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW, EvalPrediction
from transformers import pipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support
import pandas as pd
from saved_metrics.confusion_matrix import make_confusion_matrix


def classifier(model_path):
    model_name = model_path
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    return classifier

def prepare_dataset(path):
    test = pd.read_csv(path)
    test['text'] = test['text'].apply(lambda x: str(x))
    test['label'] = test["label"].apply(lambda x: int(x))
    return test

def classify(sentence):

    classifcation = antisem_classifier(sentence[:512])[0]["label"]

    if classifcation == "LABEL_0":
        return 0
    else:
        return 1

def get_metrics(y_true,y_pred):
    return {"f1_score": f1_score(y_true,y_pred,average="micro"),
            "accuracy": accuracy_score(y_true,y_pred),
            "confusion_matrix": confusion_matrix(y_true,y_pred),
            "prec_rec_fscore": precision_recall_fscore_support(y_true,y_pred)

    }

def plot_matrix(matrix,matrix_path,title):
    labels = ["True Neg","False Pos","False Neg","True Pos"]
    categories = ["nicht antisemitisch","antisemitisch"]
    make_confusion_matrix(matrix,group_names=labels,categories=categories,cmap="binary",save_path=matrix_path,title=title)


if __name__ == "__main__":
    model_path = "./models/without_slur_keywords/04_10_2021_20_20_23"
    #model_path = "./models/with_keywords/05_10_2021_10_46_14"
    #model_path = "./models/without_all_keywords/04_10_2021_16_25_23"
    antisem_classifier = classifier(model_path)

    test = prepare_dataset("../data_without_slur_keywords_test.csv")

    test['predicted'] = test['text'].apply(classify)
    y_pred = test["predicted"]
    y_true = test["label"]


    metrics = get_metrics(y_true,y_pred)
    print(metrics)

    title = "Ohne Slur-Schlüsselworte"
    matrix_path = "./saved_metrics/confusion_matrix_without_slur_keywords.png"
    plot_matrix(metrics["confusion_matrix"],matrix_path,title)




