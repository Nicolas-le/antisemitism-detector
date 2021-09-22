from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW, EvalPrediction
from transformers import pipeline
import csv
from sklearn.metrics import accuracy_score
import numpy as np
import torch
from torch.utils.data import DataLoader

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

def test_trainer():
    finalMetrics = list()
    model_name = "./models"
    model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=1)

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

    trainer = Trainer(
        model=model,  # the instantiated 🤗 Transformers model to be trained
        args=training_args,  # training arguments, defined above
        train_dataset=train_dataset,  # training dataset
        eval_dataset=val_dataset,  # evaluation dataset
        compute_metrics=hateMetrics
    )

    evaMetrics = trainer.evaluate()
    trainLoss: float = trainer.evaluate(train_dataset)['eval_loss']

    finalMetrics.append(
        {"eval_train_loss": trainLoss, **evaMetrics}
    )

    metricsTunedDf = pd.DataFrame(finalMetrics)
    print(metricsTunedDf)

test()

