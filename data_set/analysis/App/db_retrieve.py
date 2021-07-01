from tinydb import TinyDB, Query

class DBRetrieval:
    def __init__(self):
        self.whole_database = TinyDB('../4chan_pol_database.json') #path from run_app.py

    def get_thread(self, thread_id):
        Thread = Query()
        return self.whole_database.search(Thread.thread == thread_id)
