from db_retrieve import DBRetrieval
from utils import print_header, make_decision, create_keywords


class Filler():
    def __init__(self):
        self.retrieval = DBRetrieval(original_and_restuctured=True)
        self.keywords = create_keywords()
        self.last_entry = self.get_last_entry()

    def fill(self):
        print_header(self.retrieval)
        inserted_counter = 0

        for table in self.retrieval.non_kw_subset.all()[self.last_entry+1:]:
            if not self.decide(table):
                break
            inserted_counter += 1

        print("You have decided over {} comments in one session! Congrats! *_*".format(inserted_counter))
        print("#"*100)
        self.retrieval.antisemitic_subset.close()

    def decide(self,table):
        for comment_id in table:

            try:
                print("Comment ID: {}".format(comment_id))
                print(table[comment_id])
            except UnicodeEncodeError:
                print("Not readable, pls sort in unsure")
                print("!" * 30)

            decision = make_decision()

            if decision == 0:
                self.insert(comment_id,table[comment_id],0)
                print("-" * 80)
            elif decision == 5:
                print("Exiting the Tool\nLast inserted comment ID: {}".format(int(comment_id) - 1))
                return False
            else:
                self.insert(comment_id, table[comment_id], 3)
                print("Inserted to unsure, because we are searching for non antisemitic comments.")
                print("-" * 80)

            return True
    def insert(self,comment_id,comment,label):
        tmp_dictionary_for_insertion = {}

        tmp_dictionary_for_insertion[comment_id] = {
            "comment": comment,
            "label": label
        }

        self.retrieval.antisemitic_subset.insert(tmp_dictionary_for_insertion)

    def get_last_entry(self):
        last_entry = self.retrieval.antisemitic_subset.get(doc_id=len(self.retrieval.antisemitic_subset))

        try:
            last_entry = int(list(last_entry.keys())[0])
        except AttributeError:
            last_entry = -1

        return last_entry