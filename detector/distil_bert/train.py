import csv
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW, EvalPrediction
import torch
from torch.utils.data import DataLoader
import pandas as pd
import numpy as np
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split


def create_test_train(file_name):
    with open(file_name, newline='') as csv_file:
        reader = csv.DictReader(csv_file)
        texts, labels = [], []

        for row in reader:

            texts.append(row["text"])
            labels.append(int(row["label"]))
            #labels.append(row["label"])

    return train_test_split(texts, labels, test_size=.2)

def tokenize_train_test(train_texts, val_texts):
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    train_encodings = tokenizer(train_texts, truncation=True, padding=True)
    val_encodings = tokenizer(val_texts, truncation=True, padding=True)

    return train_encodings, val_encodings

class Dataset(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def hateMetrics(pred: EvalPrediction):
    """
    Compute 3 accuracies: all labels, hate, noHate. These are the baseline metrics
    used in the paper to compare models (https://arxiv.org/pdf/1809.04444.pdf, page 7).
    Function assumes 'hate' group uses label 1, 'noHate' uses label 0.

    For reference, results from paper:

      Accu | hate | noHate | all
      ---------------------------
      SVM  | 0.69 | 0.73   | 0.71
      CNN  | 0.55 | 0.79   | 0.66
      LSTM | 0.71 | 0.75   | 0.73
    """
    labels = pred.label_ids
    preds = pred.predictions.argmax(-1)

    mapper = lambda n: True if n == 1 else False

    hatePreds = preds[[mapper(l) for l in labels]]
    noHatePreds = preds[[mapper(l) for l in 1 - labels]]

    return {
      'accHate': accuracy_score(hatePreds, np.ones_like(hatePreds)),
      'accNoHate': accuracy_score(noHatePreds, np.zeros_like(noHatePreds)),
      'accAll': accuracy_score(labels, preds),
    }

def training(train_dataset,val_dataset):
    finalMetrics = list()

    training_args = TrainingArguments(
        output_dir='./results',  # output directory
        num_train_epochs=3,  # total number of training epochs
        per_device_train_batch_size=16,  # batch size per device during training
        per_device_eval_batch_size=64,  # batch size for evaluation
        warmup_steps=500,  # number of warmup steps for learning rate scheduler
        weight_decay=0.01,  # strength of weight decay
        logging_dir='./logs',  # directory for storing logs
        logging_steps=10,
    )

    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

    trainer = Trainer(
        model=model,  # the instantiated 🤗 Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=train_dataset,  # training dataset
        eval_dataset=val_dataset,  # evaluation dataset
        compute_metrics=hateMetrics
    )

    trainer.train()
    trainer.save_model("./models")
    evaMetrics = trainer.evaluate()
    trainLoss: float = trainer.evaluate(train_dataset)['eval_loss']

    finalMetrics.append(
        {"eval_train_loss": trainLoss, **evaMetrics}
    )

    metricsTunedDf = pd.DataFrame(finalMetrics)
    metricsTunedDf.to_csv("metrics_distil_bert#2.csv", sep='\t')


def main(train_source):
    train_texts, val_texts, train_labels, val_labels = create_test_train(train_source)


    train_encodings, val_encodings = tokenize_train_test(train_texts, val_texts)
    train_dataset = Dataset(train_encodings, train_labels)
    val_dataset = Dataset(val_encodings, val_labels)

    training(train_dataset,val_dataset)


#main("../data_train_without_keywords.csv")
main("../data_train.csv")