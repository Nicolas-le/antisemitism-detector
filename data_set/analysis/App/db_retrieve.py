from tinydb import TinyDB, Query
from collections import defaultdict

class DBRetrieval:
    def __init__(self):
        self.whole_database = TinyDB('../4chan_pol_database.json') #path from run_app.py
        self.detection_database = TinyDB('../detections_4chan_pol_database.json')
        self.restructured_data_set = self.get_restructured_data_set()

    def get_thread(self, thread_id):
            Thread = Query()
            return self.whole_database.search(Thread.thread == thread_id)

    def retrieve_detections_per_time_interval(self, time_interval):
        if time_interval == "hourly":
            return self.detection_database.get(doc_id=1)["hourly"]
        else:
            return self.detection_database.get(doc_id=2)["daily"]

    def get_restructured_data_set(self):
        # restructuring (should be for whole data set)
        restructured_dataset = defaultdict(dict)

        for t in self.whole_database.all():
            t = dict(t)
            thread_id = t["thread"]
            t.pop("thread")
            restructured_dataset[thread_id] = t

        return restructured_dataset



