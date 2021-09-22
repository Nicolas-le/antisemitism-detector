from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments, EvalPrediction
import torch
from torch.utils.data import DataLoader
import pandas as pd
from datetime import datetime

from util import create_test_train, tokenize_train_test, date_time_to_string
from metrics import antisem_metrics

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

def training(train_dataset,val_dataset,metric_title):
    final_metrics = list()

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
        compute_metrics=antisem_metrics
    )

    trainer.train()
    trainer.save_model("./models")
    evaluation_metrics = trainer.evaluate()
    train_loss: float = trainer.evaluate(train_dataset)['eval_loss']

    final_metrics.append(
        {"eval_train_loss": train_loss, **evaluation_metrics}
    )

    metrics_dataframe = pd.DataFrame(final_metrics)
    metrics_dataframe.to_csv("./saved_metrics/distil_bert_"+metric_title+".csv", sep='\t')


def main(train_source):
    train_texts, test_texts, train_labels, test_labels = create_test_train(train_source)


    train_encodings, val_encodings = tokenize_train_test(train_texts, test_texts)
    train_dataset = Dataset(train_encodings, train_labels)
    val_dataset = Dataset(val_encodings, test_labels)

    metric_title = date_time_to_string(datetime.now())
    training(train_dataset,val_dataset,metric_title)


#main("../data_train_without_keywords.csv")
main("../data_train.csv")