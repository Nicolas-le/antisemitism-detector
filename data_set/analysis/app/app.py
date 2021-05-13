from flask import Flask, render_template, request
from App import dataPreprocessing

app = Flask(__name__)

@app.route("/")
def home():
    return render_template('home.html')