import json, plotly

def preprocess_classification(classification):
    final_dict = {}

    if classification["label"] == "LABEL_1":
        final_dict["label"] = "Antisemitic"
        final_dict["confidence"] = str(round(classification["score"], 2)*100) +"%"
    else:
        final_dict["label"] = "Not antisemitic"
        final_dict["confidence"] = str(round(classification["score"], 2)*100) +"%"

    return final_dict


def split_into_list(string):
    return string.split(",")


def get_json_plots(plotter):

    def get_highest_thread_plots(plots):
        list_of_plots = []
        counter = 0
        for plot in plots:
            list_of_plots.append(("counter"+str(counter), json.dumps(plot, cls=plotly.utils.PlotlyJSONEncoder)))
            counter += 1

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

def get_topics_initial_comment(empath_lex, thread):

    if thread["initial_comment"]is not None:
        topics = empath_lex.analyze(thread["initial_comment"], normalize=True)

        threshold = 0.001
        if topics is not None:
            topic_dictionary = {k: v for k,v in topics.items() if v >= threshold}
        else:
            topic_dictionary = {}

        topic_dictionary = {k: v for k, v in sorted(topic_dictionary.items(), key=lambda item: item[1], reverse=True)}
        top_ten = list(topic_dictionary.items())[2:12]
    else:
        top_ten = {}

    return {
        "thread": thread["thread"],
        "initial_country": thread["initial_country"],
        "posting_time": thread["posting_time"],
        "initial_comment": thread["initial_comment"],
        "topics": top_ten,
        "replies": thread["replies"]
        }

