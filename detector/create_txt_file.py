from tinydb import TinyDB
import csv
from collections import defaultdict


class Post():
    def __init__(self, comment, label):
        #self.comment = self.remove_tokens(comment) # onyl for fasttext
        #self.label = self.convert_label(label) #only for fasttext
        self.comment = self.remove_tokens(comment)
        self.label = label

    def remove_tokens(self, comment):
        return ' '.join(word for word in comment)
    def convert_label(self, label):
        if label == 1:
            return "antisemitic"
        if label == 0:
            return "notantisemitic"
        if label == 3:
            return "unsure"

def write_to_file(writer, post):
    try:
        writer.writerow({'text': post.comment, 'label': post.label})
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
    return comment, keyword_list

def iterate_file(without_keyword,file,db):

    field_names = ['text', 'label']
    writer = csv.DictWriter(file, fieldnames=field_names)
    writer.writeheader()

    if without_keyword:
        for entry in db.all():
            entry = dict(entry)
            for i in entry.items():
                if i[1]["label"] == "unsure":
                    continue
                elif i[1]["label"] == 3:
                    continue
                comment,_ = delete_keywords(i[1]["comment"])
                post = Post(comment,i[1]["label"])
                write_to_file(writer, post)
    else:
        for entry in db.all():
            entry = dict(entry)
            for i in entry.items():
                if i[1]["label"] == "unsure":
                    continue
                elif i[1]["label"] == 3:
                    continue
                post = Post(i[1]["comment"],i[1]["label"])
                write_to_file(writer, post)

def write_random_non_posts(keyword_list,file):
    """
    Temporary function to add non antisemitic posts
    :param keyword_list:
    :param file:
    :return:
    """
    original_db = TinyDB('../data_set/4chan_pol_database.json')
    restructured_data_set = get_restructured_data_set(original_db)
    count = 0
    added_comments = 500

    writer = csv.DictWriter(file, fieldnames=['text', 'label'])

    for thread_id, thread in restructured_data_set.items():
        if not any([True for x in keyword_list if x in thread["initial_comment"]]):
            post = Post(thread["initial_comment"], 0)
            write_to_file(writer, post)

            if count == added_comments:
                break
            count += 1

def get_restructured_data_set(original_database):
    """
    Helper of write random non posts
    :param original_database:
    :return:
    """
    # restructuring (should be for whole data set)
    restructured_dataset = defaultdict(dict)

    for t in original_database.all():
        t = dict(t)
        thread_id = t["thread"]
        t.pop("thread")
        restructured_dataset[thread_id] = t

    return restructured_dataset


def main():
    db = TinyDB('../old_labeling_removed_17.09/antisemitic_subset.json')

    _,keyword_list = delete_keywords("...")

    with open("data_train_without_keywords.csv", 'w') as file:
        iterate_file(True,file,db)
        write_random_non_posts(keyword_list, file)

    with open("data_train.csv", 'w') as file:
        iterate_file(False,file,db)
        write_random_non_posts(keyword_list, file)


main()