from db_retrieve import DBRetrieval
from utils import create_keywords


def create_initial_subset():
    ID = 0
    retrieval =DBRetrieval(original_and_restuctured=True)
    keywords = create_keywords()

    for thread_id, thread in retrieval.restructured_data_set.items():
        keyword_comments = {}

        print("ID: {}".format(ID))

        if any([True for x in keywords if x in thread["initial_comment"]]):
            keyword_comments[ID] = thread["initial_comment"]
            ID += 1
            retrieval.initial_subset.insert(keyword_comments)

        for reply in thread["replies"]:
            keyword_comments = {}
            if any([True for x in keywords if x in reply["comment"]]):
                keyword_comments[ID] = reply["comment"]
                ID += 1
                retrieval.initial_subset.insert(keyword_comments)

        if ID % 5000 == 0:
            retrieval.restart_subset_db()

    retrieval.initial_subset.close()