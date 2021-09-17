from db_retrieve import DBRetrieval
from pyfiglet import Figlet

class SubsetCreator():

    def __init__(self):
        self.retrieval = DBRetrieval()
        self.keywords = self.create_keywords()
        self.last_entry = self.get_last_entry()

    def main(self):
        self.header()
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

    def header(self):
        f = Figlet(font="slant")
        print(f.renderText("FUCK ANTISEMITISM"))
        print("Label the shit out of the comments!")
        antisem = 0
        nantisem = 0
        unsure = 0

        for comment in self.retrieval.antisemitic_subset.all():
            for id in comment:
                if comment[id]["label"] == 1:
                    antisem += 1
                elif comment[id]["label"] == 0:
                    nantisem += 1
                elif comment[id]["label"] == 3:
                    unsure += 1

        print("The Database contains...\n...comments, "
              "labeled as antisemitic: {}\n...comments, labeled as not antisemitic: "
              "{}\n...and comments, labeled as unsure: {}".format(antisem,nantisem,unsure))
        print("_"*100)

    def create_keywords(self):
        kl_jewish = ["jew","jews","jewish","judaism","david"]
        kl_middle_east = ["israel","zionist","zionists","palestinian","palestinians","nationalist","hamas","idf","gaza"]
        kl_slurs = ["kike","kikes","shylock","zog","yid","zhyd","shyster","smouch","scapegoat","grug"]
        kl_racist = ["nigger","niggers","racist","migrants"]
        kl_synonyms = ["bankers","ngos","interests","globalist","greed","illuminati","nwo","academics","lobbyists"]
        kl_uncategorized = ["hitler","holocaust","whites","sand","nazi","antisemitic","clannish","control","cowardice","creatures","(((echo)))","silencing","media"]

        return kl_jewish + kl_middle_east + kl_slurs + kl_racist + kl_synonyms + kl_uncategorized


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