from flask import Flask, render_template, request
from App import dataPreprocessing
from empath import Empath

app = Flask(__name__)

@app.route("/")
def home():
    empath_lex = Empath()

    # information per hour



    return render_template('home.html')