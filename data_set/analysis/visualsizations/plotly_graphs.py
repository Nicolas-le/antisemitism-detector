import plotly.graph_objects as go
from db_retrieve import DBRetrieval

empath_lex = Empath()
spacy_en_core = spacy.load('en_core_web_sm')
retrieval = DBRetrieval()

def create_detection_graphs(time_interval):

    extracted_information = data_preprocessing.preprocess_post_per_time_interval(retrieval, time_interval)
    for key,value in extracted


create_detection_graphs("daily")