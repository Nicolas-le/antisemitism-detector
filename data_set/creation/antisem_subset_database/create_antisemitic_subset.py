from db_retrieve import DBRetrieval


class SubsetCreator():

    def __init__(self):
        self.retrieval = DBRetrieval()
        self.keywords = self.create_keywords()
        self.last_entry = self.get_last_entry()

    def main(self):

        for table in self.retrieval.initial_subset.all()[self.last_entry+1:]:
            if not self.get_antisem_comment(table):
                break

        self.retrieval.antisemitic_subset.close()

    def get_antisem_comment(self, table):

        for comment_id in table:
            antisemitic_subset = {}
            print("Comment ID: {}".format(comment_id))
            print(table[comment_id])

            decision = self.decision()

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

    def decision(self):
        print("\n1 = antisem ; 0 = not antisem, 3 = unsure, 5 = break",flush=True)

        try:
            decision = int(input())
        except ValueError:
            print("No valid decision")
            return 5

        return decision


    def create_keywords(self):
        keyword_list = ["jew","jews","bankers","kike","hitler","kikes","nigger","niggers","holocaust","whites","racist","zionist","palestinian","palestinians","ngos","migrants","shylock","jewish","interests","nationalist","sand","zog","yid"]
        return keyword_list

    def create_initial_subset(self):
        ID = 0

        for thread_id, thread in self.retrieval.restructured_data_set.items():
            keyword_comments = {}

            print("ID: {}".format(ID))

            if any([True for x in self.keywords if x in thread["initial_comment"]]):
                keyword_comments[ID] = thread["initial_comment"]
                ID += 1
                self.retrieval.initial_subset.insert(keyword_comments)

            for reply in thread["replies"]:
                keyword_comments = {}
                if any([True for x in self.keywords if x in reply["comment"]]):
                    keyword_comments[ID] = reply["comment"]
                    ID += 1
                    self.retrieval.initial_subset.insert(keyword_comments)

            if ID % 5000 == 0:

                self.retrieval.restart_subset_db()

        self.retrieval.initial_subset.close()




creator = SubsetCreator()
creator.main()
#creator.create_initial_subset()