from transformers import DistilBertForSequenceClassification, Trainer, TrainingArguments, EvalPrediction
import torch
from torch.utils.data import DataLoader
import pandas as pd
from datetime import datetime
import os

from utils import create_test_train, tokenize_train_test, date_time_to_string
from metrics import antisem_metrics

class Dataset(torch.utils.data.Dataset):
    """
    Pytorch related Dataset class
    """
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

def training(train_dataset, test_dataset, metric_title,model_directory,number_of_epochs=4):
    final_metrics = list()

    training_args = TrainingArguments(
        output_dir='./training/results',
        num_train_epochs=number_of_epochs,
        per_device_train_batch_size=16,
        per_device_eval_batch_size=64,
        warmup_steps=500,
        weight_decay=0.01,
        logging_dir='./training/logs',
        logging_steps=10,
    )

    model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased")

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        compute_metrics=antisem_metrics
    )

    trainer.train()
    trainer.save_model(model_directory)
    evaluation_metrics = trainer.evaluate()
    train_loss: float = trainer.evaluate(train_dataset)['eval_loss']

    final_metrics.append(
        {"eval_train_loss": train_loss, **evaluation_metrics}
    )

    metrics_dataframe = pd.DataFrame(final_metrics)
    metrics_dataframe.to_csv("./saved_metrics/distil_bert_epochs_"+ str(number_of_epochs) + "_" +metric_title+".csv")

def main(train_csv,test_csv, input_information):
    train_texts, test_texts, train_labels, test_labels = create_test_train(train_csv,test_csv)

    train_encodings, test_encodings = tokenize_train_test(train_texts, test_texts)
    train_dataset = Dataset(train_encodings, train_labels)
    test_dataset = Dataset(test_encodings, test_labels)

    model_directory = "./models/"+ input_information + "/" + date_time_to_string(datetime.now())
    os.mkdir(model_directory)
    metric_title = input_information + "_" + date_time_to_string(datetime.now())

    training(train_dataset,test_dataset,metric_title,model_directory,number_of_epochs=2)

#input_information = "without_all_keywords"
#train_csv, test_csv = "../data_without_all_keywords_train.csv", "../data_without_all_keywords_test.csv"
#main(train_csv, test_csv, input_information)

#input_information = "without_slur_keywords"
#train_csv, test_csv = "../data_without_slur_keywords_train.csv", "../data_without_slur_keywords_test.csv"
#main(train_csv, test_csv, input_information)

input_information = "with_keywords"
train_csv, test_csv = "../data_train.csv", "../data_test.csv"
main(train_csv, test_csv, input_information)