import requests
import json
import tinydb


def get_IDs():
    with open('pol_archive_thread_IDs.json') as thread_IDs_file:
        thread_IDs = json.load(thread_IDs_file)

    # iterating over thread_IDs_file and call get_thread_json() every second

def get_thread_Json(thread_ID):
    thread_json = requests.get("https://a.4cdn.org/pol/thread/"+str(thread_ID)+".json")
    preprocess_json(thread_json)

def preprocess_json(thread_json):
    # take whole json per thread and delete unuseful information
    store_to_db(preprocessed_json)

def store_to_db(preprocessed_json):
    # save json to tinydb


"""
iterate over every tinydb entry:

for thread in db.__iter__():
    do something with thread, f.ex.:
    db.update({'keyword': ["jew"]}, doc_ids=[thread.doc_id])
    https://tinydb.readthedocs.io/en/stable/usage.html
    works even if keyword isn't originally a key in the thread

    db.close() wichtig für schreiben von Änderungen
"""
