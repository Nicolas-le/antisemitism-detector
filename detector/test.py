from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments, AdamW
from transformers import pipeline

def test():
    model_name = "./models"
    model = DistilBertForSequenceClassification.from_pretrained(model_name, num_labels=1)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    print(classifier("I just like the way it looks man. The sun is out, so cool my boi."))

test()

