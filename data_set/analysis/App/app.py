from flask import Flask, render_template, request
from App.db_retrieve import DBRetrieval
from App.plotly_graphs import Plotting
import json
import plotly as go


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

@app.route("/plots", methods=['POST',"GET"])
def plots():
    plotter = Plotting("daily", retrieval)

    topic_plot_json = json.dumps(plotter.topic_plot, cls=go.utils.PlotlyJSONEncoder)

    #graphJSON = json.dumps(data, cls=go.utils.PlotlyJSONEncoder)

    return render_template('plots.html', topic_plot_json=topic_plot_json)


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message),flush=True)

    return dict(mdebug=print_in_console)


