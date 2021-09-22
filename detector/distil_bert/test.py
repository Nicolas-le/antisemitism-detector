from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW, EvalPrediction
from transformers import pipeline
import csv


def classifier():
    model_name = "./models"
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    return classifier

def test():

    antisem_classifier = classifier()


    with open("../data_train.csv",newline='') as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            decision = antisem_classifier(row["text"])
            real_label = row["label"]

            print(decision,flush=True)
            print(real_label,flush=True)



antisem_classifier = classifier()

test_sent = "I fucking hate these bankers, also the israelis controlling the international money traffic"
print(antisem_classifier(test_sent))

