from tinydb import TinyDB, Query
from collections import defaultdict
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

class DBRetrieval:
    def __init__(self):
        #self.original_database = TinyDB('../../4chan_pol_database.json') #path from run_app.py
        self.antisemitic_subset = TinyDB('../../antisemitic_subset.json')
        self.initial_subset = TinyDB("./initial_subset.json", storage=CachingMiddleware(JSONStorage))
        #self.restructured_data_set = self.get_restructured_data_set()

    def get_restructured_data_set(self):
        # restructuring (should be for whole data set)
        restructured_dataset = defaultdict(dict)

        for t in self.original_database.all():
            t = dict(t)
            thread_id = t["thread"]
            t.pop("thread")
            restructured_dataset[thread_id] = t

        return restructured_dataset

    def restart_subset_db(self):
        print("Restart Subset DB", flush=True)
        self.initial_subset.close()
        self.initial_subset = TinyDB("./initial_subset.json", storage=CachingMiddleware(JSONStorage))


