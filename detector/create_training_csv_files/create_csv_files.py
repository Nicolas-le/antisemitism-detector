from tinydb import TinyDB
import os

from post import Post
from utils import write_to_file, get_slur_keywords, get_all_keywords, delete_keywords, get_writer

def create_train_with_keywords(path, database):
    writer = get_writer(path)

    for entry in database.all():
        entry = dict(entry)
        for i in entry.items():
            if skip_unsure_labels(i[1]["label"]):
                continue
            post = Post(i[1]["comment"],i[1]["label"])
            write_to_file(writer, post)


def create_train_without_all_keywords(path, database):
    writer = get_writer(path)
    keyword_list = get_all_keywords()

    for entry in database.all():
        entry = dict(entry)
        for i in entry.items():
            if skip_unsure_labels(i[1]["label"]):
                continue

            comment = delete_keywords(i[1]["comment"],keyword_list)
            post = Post(comment, i[1]["label"])
            write_to_file(writer, post)

def create_train_without_slur_keywords(path, database):
    writer = get_writer(path)
    keyword_list = get_slur_keywords()

    for entry in database.all():
        entry = dict(entry)
        for i in entry.items():
            if skip_unsure_labels(i[1]["label"]):
                continue

            comment = delete_keywords(i[1]["comment"],keyword_list)
            post = Post(comment, i[1]["label"])
            write_to_file(writer, post)


def skip_unsure_labels(label):
    if label == "unsure" or label == 3:
        return True
    else:
        False


def main():
    database = TinyDB('../data_set/antisemitic_subset.json')

    with open("data_train.csv", 'w') as path:
        create_train_with_keywords(path, database)

    with open("data_train_without_all_keywords.csv", 'w') as path:
        create_train_without_all_keywords(path, database)

    with open("data_train_without_slur_keywords.csv", 'w') as path:
        create_train_without_slur_keywords(path, database)


main()