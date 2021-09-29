from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW, EvalPrediction
from transformers import pipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support
import pandas as pd
from sklearn.model_selection import train_test_split
from saved_metrics.confusion_matrix import make_confusion_matrix


def classifier(model_path):
    model_name = model_path
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    return classifier

def prepare_dataset(path):
    dataset = pd.read_csv(path)
    return train_test_split(dataset,test_size=0.2,random_state=42)

def classify(sentence):

    classifcation = antisem_classifier(sentence[:512])[0]["label"]

    if classifcation == "LABEL_0":
        return 0
    else:
        return 1

def get_metrics(y_true,y_pred):
    return {"f1_score": f1_score(y_true,y_pred),
            "accuracy": accuracy_score(y_true,y_pred),
            "confusion_matrix": confusion_matrix(y_true,y_pred),
            "prec_rec_fscore": precision_recall_fscore_support(y_true,y_pred)

    }

def plot_matrix(matrix,matrix_path):
    labels = ["True Neg","False Pos","False Neg","True Pos"]
    categories = ["antisemitisch","nicht antisemitisch"]
    make_confusion_matrix(matrix,group_names=labels,categories=categories,cmap="binary",save_path=matrix_path)


if __name__ == "__main__":
    model_path = "./models/with_keywords/28_09_2021_19_34_44"
    antisem_classifier = classifier(model_path )

    train, test = prepare_dataset("../data_train.csv")

    test['predicted'] = test['text'].apply(classify)
    y_pred = test["predicted"]
    y_true = test["label"]


    metrics = get_metrics(y_true,y_pred)
    print(metrics)

    matrix_path = "./saved_metrics/confusion_matrix_with_all_keywords.png"
    #plot_matrix(metrics["confusion_matrix"],matrix_path)




