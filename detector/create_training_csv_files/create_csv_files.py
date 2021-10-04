from tinydb import TinyDB
from sklearn.model_selection import train_test_split
import pandas as pd

from post import Post
from utils import get_slur_keywords, get_all_keywords, delete_keywords

def create_test_train_sets(path, database, deletion=False, keyword_list=[]):
    df_complete = pd.DataFrame(columns=["text","label"])

    for entry in database.all():
        entry = dict(entry)
        for i in entry.items():
            if skip_unsure_labels(i[1]["label"]):
                continue

            if deletion:
                comment = delete_keywords(i[1]["comment"], keyword_list)
            else:
                comment = i[1]["comment"]

            post = Post(comment,i[1]["label"])
            df_complete = df_complete.append({"text":post.comment,"label":post.label},ignore_index=True)


    train, test = train_test_split(df_complete,test_size=0.2,random_state=42)

    train.to_csv(path+"train.csv")
    test.to_csv(path+"test.csv")

def skip_unsure_labels(label):
    if label == "unsure" or label == 3:
        return True
    else:
        False


def main():
    database = TinyDB('../../data_set/antisemitic_subset.json')

    create_test_train_sets("../data_", database)
    create_test_train_sets("../data_without_all_keywords_", database, deletion=True,keyword_list=get_all_keywords())
    create_test_train_sets("../data_without_slur_keywords_", database, deletion=True,keyword_list=get_slur_keywords())


main()