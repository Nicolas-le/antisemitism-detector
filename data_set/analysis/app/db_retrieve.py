from tinydb import TinyDB, Query


class DBRetrieval:
    def __init__(self):
        self.database = TinyDB('../../4chan_pol_database.json')

    def get_post_per_day(self,date):
        # "posting_time": "05/12/21(Wed)06:12:07"
        query = Query()
        return self.database.search(query["posting_time"] == date)

retrieval = DBRetrieval()

posts_of_date = retrieval.get_post_per_day("05/12/21(Wed)06:12:07")
