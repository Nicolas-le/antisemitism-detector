from flask import Flask, render_template, request
from App import data_preprocessing
from collections import defaultdict

app = Flask(__name__)
empath_lex = Empath()
spacy_en_core = spacy.load('en_core_web_sm')

@app.route("/", methods=['GET', 'POST'])
def home():

    # information per hour
    time_interval = "daily" # hourly, daily
    #time_interval = request.form.get('comp_select')

    extracted_information = get_data(time_interval)

    print(extracted_information, flush=True)

    return render_template('home.html')

def get_data(time_interval):
    dates = data_preprocessing.get_dates(time_interval)
    print(dates,flush=True)

    extracted_information = defaultdict(dict)
    print(len(dates),flush=True)
    counter = 0
    for date in dates:
        print(counter,flush=True)
        counter += 1
        extracted_information[date] = data_preprocessing.get_info_per_date(date,empath_lex,spacy_en_core)

    return extracted_information

