from db_retrieve import DBRetrieval
from utils import print_header, create_keywords, make_decision

class SubsetCreator():

    def __init__(self):
        self.retrieval = DBRetrieval()
        self.keywords = create_keywords()
        self.last_entry = self.get_last_entry()

    def create_subset(self):
        print_header(self.retrieval)
        inserted_counter = 0

        for table in self.retrieval.initial_subset.all()[self.last_entry+1:]:
            if not self.get_antisem_comment(table):
                break
            inserted_counter += 1

        print("You have inserted {} comments in one session! Congrats! *_*".format(inserted_counter))
        print("#"*100)
        self.retrieval.antisemitic_subset.close()

    def get_antisem_comment(self, table):

        for comment_id in table:
            antisemitic_subset = {}

            try:
                print("Comment ID: {}".format(comment_id))
                print("Keywords of post: {}".format(self.get_containing_keywords(table[comment_id])))
                print(table[comment_id])
            except UnicodeEncodeError:
                print("Not readable, pls sort in unsure")
                print("!"*30)

            decision = make_decision()

            if decision == 1:
                antisemitic_subset[comment_id] = {
                    "comment": table[comment_id],
                    "label": 1
                }
            elif decision == 0:
                antisemitic_subset[comment_id] = {
                    "comment": table[comment_id],
                    "label": 0
                }
            elif decision == 3:
                antisemitic_subset[comment_id] = {
                    "comment": table[comment_id],
                    "label": 3
                }
            elif decision == 5:
                print("Exiting the Tool\nLast inserted comment ID: {}".format(int(comment_id)-1))
                return False

            self.retrieval.antisemitic_subset.insert(antisemitic_subset)
            print("-"*80)
            return True

    def get_last_entry(self):
        last_entry = self.retrieval.antisemitic_subset.get(doc_id=len(self.retrieval.antisemitic_subset))
        try:
            last_entry = int(list(last_entry.keys())[0])
        except AttributeError:
            last_entry = -1

        return last_entry

    def get_containing_keywords(self, comment):
        containing_keywords = []

        for word in comment:
            if word in self.keywords:
                containing_keywords.append(word)
            else:
                continue

        return ' '.join(list(set(containing_keywords)))




