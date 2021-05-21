import requests as r
import json
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb.operations import add, delete
from time import time, sleep
import data_cleaner
import spacy


def get_IDs():
    # iterating over thread_IDs_file and call get_thread_json() every second
    with open('pol_archive_thread_IDs.json') as thread_IDs_file:
        thread_IDs = json.load(thread_IDs_file)
        return thread_IDs  

def get_thread_Json(thread_ID,tokenizer):

    # handle connection error request exceptions
    try:
        thread = r.get("https://a.4cdn.org/pol/thread/"+str(thread_ID)+".json")
    except r.exceptions.RequestException as e:
       return False

    thread = thread_sanity_check(thread,tokenizer)
    return thread


def thread_sanity_check(thread,tokenizer):
    # 1. Test if response body contains sth.
    if thread.status_code == 404:
        return False
    if not thread.text:
        return False

    # 2. Handle error if deserialization fails (because of no text or bad format)
    try:
        thread_json = thread.json()

        # 3. check that .json() did NOT return an empty dict
        if not thread_json:
            return False

    except ValueError:
        return False

    return preprocess_json(thread.json(),tokenizer)
   

def preprocess_json(thread_json,tokenizer):
    def handle_replies(posts,tokenizer):
        output_list = []
        for post in posts:
            tmp_dict = {
                "country": post.get("country_name"),
                "posting_time": post.get("now"),
                "comment": data_cleaner.clean_comment(post.get("com"),tokenizer)
            }

            if data_cleaner.check_appending(tmp_dict):
                output_list.append(tmp_dict)
            else:
                continue

        return output_list

    preprocessed_json = {
        "thread": thread_json["posts"][0].get("no"),
        "initial_country": thread_json["posts"][0].get("country_name"),
        "posting_time": thread_json["posts"][0].get("now"),
        "initial_comment": data_cleaner.clean_comment(thread_json["posts"][0].get("com"),tokenizer),
        "replies": handle_replies(thread_json["posts"][1:],tokenizer) # give handle_replies() all the following posts after initial post
    }

    return preprocessed_json

def store_to_db(db, preprocessed_json):
    db.insert(preprocessed_json)

def main():
    db = TinyDB('../4chan_pol_database.json', storage=CachingMiddleware(JSONStorage))
    thread_IDs = get_IDs()

    last_element_previous_list = 321324355

    thread_counter = 0
    first_fail = True

    tokenizer = spacy.load("en_core_web_sm")

    for thread_ID in reversed(thread_IDs):
        
        if thread_ID == last_element_previous_list:
            print("All new Posts have been scraped. Exiting...")
            break

        preprocessed_thread = get_thread_Json(thread_ID,tokenizer)

        if not preprocessed_thread:
            if first_fail:
                print("Thread %d isn't available anymore. Trying one more...\n" % thread_ID)
                first_fail = False
                continue
            else:
                print("Thread %d is also not available anymore. Leaving" % thread_ID)
                break

        store_to_db(db,preprocessed_thread)

        if thread_counter % 30 == 0 and thread_counter > 0:
            print(thread_counter,flush=True)

        thread_counter += 1
        sleep(1.5 - time() % 1.5)

    db.close()

main()