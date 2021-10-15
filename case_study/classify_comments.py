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

def classify_and_count(classifier, json_file):
    final_dictionary = {}

    for video_id, value in json_file.items():
        antisem_counter = 0
        prob_antisem_counter = 0
        maybe_antisem_counter = 0
        not_antisem_counter = 0
        prob_not_antisem_counter = 0
        maybe_not_antisem_counter = 0

        for comment in value["top_level_comments"]:
            classification = classifier(comment[:512])[0]

            if classification["label"] == "LABEL_1" and classification["score"] >= 0.9:
                antisem_counter += 1

                if value["title"] == "Israelis: Is international media biased against Israel?":
                    print(comment)
                    print(classification)

            elif classification["label"] == "LABEL_1" and classification["score"] < 0.9:
                prob_antisem_counter += 1
            elif classification["label"] == "LABEL_1" and classification["score"] < 0.80:
                maybe_antisem_counter += 1
            elif classification["label"] == "LABEL_0" and classification["score"] < 0.9:
                prob_not_antisem_counter += 1
            elif classification["label"] == "LABEL_0" and classification["score"] < 0.80:
                maybe_not_antisem_counter += 1
            else:
                not_antisem_counter+= 1

        final_dictionary[video_id] ={
            "title": value["title"],
            "Antisemitisch": antisem_counter,
            "Wahrscheinlich antisemitisch": prob_antisem_counter,
            "Vielleicht antisemitisch": maybe_antisem_counter,
            "Nicht antisemitisch": not_antisem_counter,
            "Wahrscheinlich nicht antisemitisch": prob_not_antisem_counter,
            "Vielleicht nicht antisemitisch": maybe_not_antisem_counter
        }

    return final_dictionary

def calculate_mean(video_dict):
    antisem_whole = 0
    not_antisem_whole = 0

    for video_id, video_information in video_dict.items():
        antisem_whole += (video_information["Antisemitisch"] + video_information["Wahrscheinlich antisemitisch"] + video_information["Vielleicht antisemitisch"])
        not_antisem_whole += (video_information["Nicht antisemitisch"] + video_information["Wahrscheinlich nicht antisemitisch"] + video_information["Vielleicht nicht antisemitisch"])

    mean_antisem = antisem_whole/ (antisem_whole + not_antisem_whole)
    mean_not_antisem = not_antisem_whole / (antisem_whole + not_antisem_whole)

    print("Mean antisem: {}; Mean not antisem: {}".format(mean_antisem,mean_not_antisem))


def main():
    classifier = get_classifier("./resources/distilbert_model")
    json_file = get_json("./resources/collected_comments_corey_whole.json")
    final_dictionary = classify_and_count(classifier, json_file)

    #plot_antisem_proportions(final_dictionary)

    calculate_mean(final_dictionary)

main()