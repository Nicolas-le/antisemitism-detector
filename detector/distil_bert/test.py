from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from transformers import pipeline
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, precision_recall_fscore_support
import pandas as pd
pd.set_option('display.max_columns', None)
from saved_metrics.confusion_matrix import make_confusion_matrix
import sys

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

def write_false_pos(df_test_with_predicted):
    """
    Saves all the false pos comments to a specific csv file. Used for a question in the thesis.
    """
    false = df_test_with_predicted.loc[df_test_with_predicted["predicted"] != df_test_with_predicted["label"]]
    false_pos = false.loc[false["label"] == 0]
    print(false_pos.head(50))
    false_pos.to_csv("./saved_metrics/false_pos_trained_with_kws.csv")

def command_line_and_start():
    fail_line = "\nWrong or no Input. You have to chose a dataset. Exiting...\n"
    try:
        decision = int(sys.argv[1])
        if decision == 1:
            model_path = "./models/with_keywords/20_10_2021_17_52_36"
            title = "Mit Schlüsselworten"
            matrix_path = "./saved_metrics/confusion_matrix_with_keywords.png"
        elif decision == 2:
            model_path = "./models/without_all_keywords/04_10_2021_16_25_23"
            title = "Ohne Schlüsselworte"
            matrix_path = "./saved_metrics/confusion_matrix_without_all_keywords.png"
        elif decision == 3:
            model_path = "./models/without_slur_keywords/04_10_2021_20_20_23"
            title = "Ohne Slur-Schlüsselworte"
            matrix_path = "./saved_metrics/confusion_matrix_without_slur_keywords.png"
        else:
            print(fail_line)
            sys.exit()
    except IndexError:
        print(fail_line)
        sys.exit()
    except ValueError:
        print(fail_line)
        sys.exit()

    return model_path, title, matrix_path


if __name__ == "__main__":

    # initialize classifier and test set
    model_path, title, matrix_path = command_line_and_start()
    antisem_classifier = classifier(model_path)
    test = prepare_dataset("../data_test.csv")

    # get predicted target variables and true labels
    test['predicted'] = test['text'].apply(classify)
    y_pred = test["predicted"]
    y_true = test["label"]

    # a function that you don't use normally.
    #write_false_pos(test)

    metrics = get_metrics(y_true,y_pred)
    print(metrics)

    plot_matrix(metrics["confusion_matrix"], matrix_path, title)






