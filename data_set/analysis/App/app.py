from flask import Flask, render_template, request
from App.db_retrieve import DBRetrieval
from App.plotly_graphs import Plotting
import json
import plotly


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

    time_interval = request.form.get('comp_select')

    if time_interval is None:
        time_interval = "daily"

    plotter = Plotting(time_interval, retrieval)
    plots =  get_json_plots(plotter)
    print(len(plots["keyword_plots"]["highest_thread_plot"]),flush=True)

    return render_template('plots.html', plots=plots)


@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(str(message),flush=True)

    return dict(mdebug=print_in_console)


def get_json_plots(plotter):

    def get_highest_thread_plots(plots):
        list_of_plots = []
        counter = 0
        for plot in plots:
            list_of_plots.append(("counter"+str(counter), json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)))
            counter += 1

        print(list_of_plots,flush=True)
        return list_of_plots

    plots = {
        "topic_plot_json": json.dumps(plotter.topic_plot, cls=plotly.utils.PlotlyJSONEncoder),
        "counting_plots": {
            "count_replies": json.dumps(plotter.counting_plots["count_replies"], cls=plotly.utils.PlotlyJSONEncoder),
            "counts": json.dumps(plotter.counting_plots["counts"], cls=plotly.utils.PlotlyJSONEncoder),
            "special_threads": json.dumps(plotter.counting_plots["special_threads"], cls=plotly.utils.PlotlyJSONEncoder)
        },
        "keyword_plots": {
            "percentage_of_keyword_occ": json.dumps(plotter.keyword_distr_plots["percentage_of_keyword_occ"], cls=plotly.utils.PlotlyJSONEncoder),
            "highest_thread_plot": get_highest_thread_plots(plotter.keyword_distr_plots["highest_thread_plot"])
        }
    }

    return plots
