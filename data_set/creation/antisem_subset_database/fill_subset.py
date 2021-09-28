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
        comment_id = self.last_entry +1

        for thread_id, thread in self.retrieval.restructured_data_set.items():

            if not self.is_there_a_keyword(thread["initial_comment"]):
                if self.decide(comment_id,thread["initial_comment"]):
                    inserted_counter += 1
                    comment_id += 1
                else:
                    break


        print("You have decided over {} comments in one session! Congrats! *_*".format(inserted_counter))
        print("#"*100)
        self.retrieval.antisemitic_subset.close()

    def is_there_a_keyword(self,comment):
        if any([True for x in self.keywords if x in comment]):
            return True
        else:
            return False

    def decide(self,comment_id,comment):
        try:
            print("Comment ID: {}".format(comment_id))
            print(comment)
        except UnicodeEncodeError:
            print("Not readable, pls sort in unsure")
            print("!" * 30)

        decision = make_decision()

        if decision == 0:
            self.insert(comment_id,comment,0)
        elif decision == 5:
            print("Exiting the Tool\nLast inserted comment ID: {}".format(int(comment_id) - 1))
            return False
        else:
            print("Not inserted, because we are searching for non antisemitic comments.")

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