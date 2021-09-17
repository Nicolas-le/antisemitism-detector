from tinydb import TinyDB
import csv

class Post():
    def __init__(self, comment, label):
        #self.comment = self.remove_tokens(comment) # onyl for fasttext
        #self.label = "__label__" + self.convert_label(label) #only for fasttext
        self.comment = self.remove_tokens(comment)
        self.label = label

    def remove_tokens(self, comment):
        return ' '.join(word for word in comment)
    def convert_label_fasttext(self, label):
        if label == 1:
            return "antisemitic"
        if label == 0:
            return "notantisemitic"
        if label == 3:
            return "unsure"

def write_to_file(writer, post):
    try:
        writer.writerow({'comment': post.comment, 'label': post.label})
    except UnicodeEncodeError:
        pass

def delete_keywords(comment):

    kl_jewish = ["jew","jews","jewish","judaism","david"]
    kl_middle_east = ["israel","zionist","zionists","palestinian","palestinians","nationalist","hamas","idf","gaza"]
    kl_slurs = ["kike","kikes","shylock","zog","yid","zhyd","shyster","smouch","scapegoat","grug"]
    kl_racist = ["nigger","niggers","racist","migrants"]
    kl_synonyms = ["bankers","ngos","interests","globalist","greed","illuminati","nwo","academics","lobbyists"]
    kl_uncategorized = ["hitler","holocaust","whites","sand","nazi","antisemitic","clannish","control","cowardice","creatures","(((echo)))","silencing","media"]

    keyword_list = kl_jewish + kl_middle_east + kl_slurs + kl_racist + kl_synonyms + kl_uncategorized
    comment = [word for word in comment if not word in keyword_list]
    return comment

def iterate_file(without_keyword,file_name,db):


    with open(file_name, 'w') as file:
        field_names = ['comment', 'label']
        writer = csv.DictWriter(file, fieldnames=field_names)
        writer.writeheader()

        if without_keyword:
            for entry in db.all():
                entry = dict(entry)
                for i in entry.items():
                    comment = delete_keywords(i[1]["comment"])
                    post = Post(comment,i[1]["label"])
                    write_to_file(writer, post)
        else:
            for entry in db.all():
                entry = dict(entry)
                for i in entry.items():
                    post = Post(i[1]["comment"],i[1]["label"])
                    write_to_file(writer, post)

def main():
    db = TinyDB('../data_set/antisemitic_subset.json')

    iterate_file(True,"data_train_without_keywords.csv",db)
    iterate_file(False,"data_train.csv",db)


main()