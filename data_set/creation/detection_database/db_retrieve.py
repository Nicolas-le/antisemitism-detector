from tinydb import TinyDB, Query


class DBRetrieval:
    def __init__(self):
        self.database = TinyDB('../../4chan_pol_database.json')
        self.test_contains = lambda value, search: search in value

    def get_post_per_day(self,date):
        # "posting_time": "05/12/21"
        query = Query()
        return self.database.search(query.posting_time.test(self.test_contains, date))

        # two_conditions
        #return self.database.search(query.posting_time.test(self.test_contains, date) & query.posting_time.test(self.test_contains, "01:41:55"))

    def get_db_all(self):
        return self.database.all()