from tinydb import TinyDB, Query, where


class DBRetrieval:
    def __init__(self):
        self.database = TinyDB('../../4chan_pol_database.json')
        self.test_contains = lambda value, search: search in value


    def get_post_per_day(self,date):
        # "posting_time": "05/12/21"
        query = Query()
        return self.database.search(query.posting_time.test(self.test_contains, date))


retrieval = DBRetrieval()
date = "05/12/21"
posts_of_date = retrieval.get_post_per_day(date)
