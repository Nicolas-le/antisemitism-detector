from flask import Flask, render_template, request
from App.db_retrieve import DBRetrieval


app = Flask(__name__)
retrieval = DBRetrieval()

@app.route("/", methods=['POST',"GET"])
def home():

    thread_id = request.form.get('fname')

    if thread_id:
        thread = retrieval.get_thread(int(thread_id))[0]
    else:
        thread = {}
    return render_template('home.html', thread=thread)

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message),flush=True)

    return dict(mdebug=print_in_console)


