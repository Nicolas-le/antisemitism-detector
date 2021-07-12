import data_preprocessing
from collections import defaultdict
import spacy
from empath import Empath
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware


empath_lex = Empath()
spacy_en_core = spacy.load('en_core_web_sm')

def get_data(time_interval):
    db = TinyDB('../detections_4chan_pol_database.json', storage=CachingMiddleware(JSONStorage))

    dates = data_preprocessing.get_dates(time_interval)
    print(dates,flush=True)

    extracted_information = defaultdict(dict)

    print(len(dates),flush=True)
    counter = 0

    for date in dates:
        print(counter,flush=True)
        counter += 1
        extracted_information[time_interval][date] = data_preprocessing.get_info_per_date(date, empath_lex, spacy_en_core)

        #print(extracted_information,flush=True)

    db.insert(extracted_information)
    db.close()


get_data("hourly")
get_data("daily")