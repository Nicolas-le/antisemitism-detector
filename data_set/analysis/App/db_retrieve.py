from tinydb import TinyDB, Query

class DBRetrieval:
    def __init__(self):
        self.whole_database = TinyDB('../4chan_pol_database.json') #path from run_app.py
        self.detection_database = TinyDB('../detections_4chan_pol_database.json')

    def get_thread(self, thread_id):
            Thread = Query()
            return self.whole_database.search(Thread.thread == thread_id)

    def retrieve_detections_per_time_interval(self, time_interval):
        if time_interval == "hourly":
            return self.detection_database.get(doc_id=1)["hourly"]
        else:
            return self.detection_database.get(doc_id=2)["daily"]
