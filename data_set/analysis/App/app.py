from flask import Flask, render_template, request
import json
import plotly
import spacy
from empath import Empath
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, pipeline

import App.data_preprocessing
from App.db_retrieve import DBRetrieval
from App.plotly_graphs import Plotting
from App.utils import preprocess_classification, split_into_list, get_json_plots, get_topics_initial_comment

app = Flask(__name__)
retrieval = DBRetrieval()
spacy_en_core = spacy.load('en_core_web_sm')
empath_lex = Empath()

def get_classifier():
    model_name = "./App/classifier_model"
    model = DistilBertForSequenceClassification.from_pretrained(model_name)
    tokenizer = DistilBertTokenizerFast.from_pretrained('distilbert-base-uncased')
    classifier = pipeline('text-classification', model=model, tokenizer=tokenizer)

    return classifier

antisem_classifier = get_classifier()

@app.route("/", methods=['POST',"GET"])
def home():

    thread_id = request.form.get('fname')

    if thread_id:
        thread = retrieval.get_thread(int(thread_id))[0]
        thread = get_topics_initial_comment(empath_lex,thread)
    else:
        thread = {}
    return render_template('home.html', thread=thread)

@app.route("/plots", methods=['POST',"GET"])
def plots():

    time_interval = request.form.get('comp_select')

    if time_interval is None:
        time_interval = "daily"

    plotter = Plotting(time_interval, retrieval)
    plots =  get_json_plots(plotter)

    return render_template('plots.html', plots=plots)

@app.route("/keyword", methods=['POST',"GET"])
def keyword():
    keyword_string = request.form.get('keyword_string')

    if keyword_string is not None:
        keyword_list = split_into_list(keyword_string)
    else:
        keyword_list = ["jew", "kike", "zionist", "israel", "shylock", "yid"]

    highest_cooc_words = App.data_preprocessing.get_keyword_information(retrieval, spacy_en_core, keyword_list)


    return render_template('keyword.html', highest_cooc_words=highest_cooc_words)

@app.route("/classifier", methods=['POST',"GET"])
def classifier():
    input_string = request.form.get('input_string')

    if input_string is not None:
        classification = preprocess_classification(antisem_classifier(input_string)[0])
    else:
        classification = {"label":"","confidence":""}


    return render_template('classifier.html', classification=classification)


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message),flush=True)

    return dict(mdebug=print_in_console)



