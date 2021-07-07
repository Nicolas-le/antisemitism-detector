import plotly.graph_objects as go
from db_retrieve import DBRetrieval
import data_preprocessing


retrieval = DBRetrieval()

def create_detection_graphs(time_interval):

    extracted_information = data_preprocessing.preprocess_post_per_time_interval(retrieval, time_interval)

    dates = []
    topics = []
    for key,value in extracted_information.items():
        dates.append(key)
        topics.append(value["topic_distr"])

    count_replies = ["count","replies"]
    counts = ["word_count_total", "word_count_without_stopwords"]
    counting_plot(extracted_information, count_replies)
    counting_plot(extracted_information, counts)


#topic_plot(topics, extracted_information, time_interval)

def topic_plot(topic_distr, extracted_info,time_interval):

    def build_topic_list():
        all_topics = []
        for thread in topic_distr:
            for topic in thread:
                all_topics.append(topic[0])

        return list(set(all_topics))

    all_topics = build_topic_list()
    data = []


    for topic in all_topics:
        dates = []
        values = []
        for date, value in extracted_info.items():
            for day_topic in value["topic_distr"]:
                if topic == day_topic[0]:
                    dates.append(date)
                    values.append(day_topic[1])

        data.append(go.Bar(name=topic, x=dates, y=values))

    layout = go.Layout(
        autosize=False,
        width=1920,
        height=1080
    )
    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(barmode='stack')
    #fig.write_image("./plots/topics_"+time_interval+".png")
    fig.show()

def counting_plot(extracted_info, concepts):
    data = []
    layout = go.Layout(
        autosize=False,
        width=1920,
        height=1080
    )

    for concept in concepts:
        dates = []
        values = []
        for date, value in extracted_info.items():
            for conc, val in value["countings"]["thread_general"].items():
                if concept == conc:
                    dates.append(date)
                    values.append(val)

        data.append(go.Bar(name=concept, x=dates, y=values))

    fig = go.Figure(data=data, layout=layout)
    fig.update_layout(barmode='group')
    #fig.write_image("./plots/topics_"+time_interval+".png")
    fig.show()



create_detection_graphs("daily")
#create_detection_graphs("hourly")