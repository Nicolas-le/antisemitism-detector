import json
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
from transformers import pipeline
import sys
sys.stdout.reconfigure(encoding='utf-8')

from plotting import plot_antisem_proportions

def get_classifier(model_path):
    model_name = model_path
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    return classifier

def get_json(path):
    with open(path) as f:
        data = json.load(f)
    return data

def get_final_dict(classifier,json_file):
    final_dictionary = {}

    for video_id, value in json_file.items():
        antisem_counter = 0
        prob_antisem_counter = 0
        maybe_antisem_counter = 0
        not_antisem_counter = 0

        for comment in value["top_level_comments"]:
            classification = classifier(comment)[0]

            if classification["label"] == "LABEL_1" and classification["score"] >= 0.9:
                antisem_counter += 1
            elif classification["label"] == "LABEL_1" and classification["score"] <= 0.9:
                prob_antisem_counter += 1
            elif classification["label"] == "LABEL_1" and classification["score"] <= 0.79:
                maybe_antisem_counter += 1
            else:
                not_antisem_counter += 1

        final_dictionary[video_id] ={
            "title": value["title"],
            "antisemitic": antisem_counter,
            "probably_antisemitic": prob_antisem_counter,
            "maybe_antisemitic": maybe_antisem_counter,
            "not_antisemitic": not_antisem_counter
        }

    return final_dictionary


def main():
    classifier = get_classifier("./resources/distilbert_model")
    json_file = get_json("./resources/collected_comments_al_jazeera.json")
    final_dictionary = get_final_dict(classifier,json_file)

    plot_antisem_proportions(final_dictionary)

main()