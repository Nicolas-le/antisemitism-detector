from flask import Flask, render_template, request
from App import data_preprocessing
from App.db_retrieve import DBRetrieval
from empath import Empath
import spacy


app = Flask(__name__)
empath_lex = Empath()
spacy_en_core = spacy.load('en_core_web_sm')
retrieval = DBRetrieval()

@app.route("/", methods=['GET', 'POST'])
def home():

    # information per hour
    #time_interval = "daily" # hourly, daily
    time_interval = request.form.get('comp_select')
    dates = []

    extracted_information = data_preprocessing.preprocess_post_per_time_interval(retrieval, time_interval)
    for key,value in extracted_information.items():
        dates.append(key)

    print(dates)

    return render_template('home.html',dates=dates, extracted_information=extracted_information)


