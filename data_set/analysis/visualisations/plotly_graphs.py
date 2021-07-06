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


    topic_plot(dates, topics)

def topic_plot(dates, topic_distr):

    data = []

    for emotion in topic_distr:
        data.append(go.Bar(name=emotion, x=dates, y=[]))





    fig = go.Figure(data=[
        go.Bar(name='SF Zoo', x=dates, y=[20, 14, 23]),
        go.Bar(name='LA Zoo', x=animals, y=[12, 18, 29])
    ])
    # Change the bar mode
    fig.update_layout(barmode='stack')
    fig.show()



create_detection_graphs("daily")
#create_detection_graphs("hourly")