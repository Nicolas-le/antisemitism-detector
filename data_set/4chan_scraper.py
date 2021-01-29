import requests as r
import json
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb.operations import add, delete
from time import time, sleep
import data_cleaner


def get_IDs():
    # iterating over thread_IDs_file and call get_thread_json() every second
    with open('pol_archive_thread_IDs.json') as thread_IDs_file:
        thread_IDs = json.load(thread_IDs_file)
        return thread_IDs  

def get_thread_Json(thread_ID):
    
    thread = r.get("https://a.4cdn.org/pol/thread/"+str(thread_ID)+".json")

    if not thread.status_code == 404:
        return preprocess_json(thread.json()), thread_ID
    else:
        return False, thread_ID

def preprocess_json(thread_json):
    def handle_replies(posts):
        output_list = []
        for post in posts:
            tmp_dict = {
                "country": post.get("country_name"),
                "posting_time": post.get("now"),
                "comment": data_cleaner.clean_comment(post.get("com"))
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
        "initial_comment": data_cleaner.clean_comment(thread_json["posts"][0].get("com")),
        "replies": handle_replies(thread_json["posts"][1:]) # give handle_replies() all the following posts after initial post
    }

    return preprocessed_json

def store_to_db(db, preprocessed_json):
    db.insert(preprocessed_json)

def main():
    db = TinyDB('4chan_pol_database.json', storage=CachingMiddleware(JSONStorage))
    thread_IDs = get_IDs()

    last_element_previous_list = 305641075

    thread_counter = 0
    for thread_ID in reversed(thread_IDs):
        
        if thread_ID == last_element_previous_list:
            print("All new Posts have been scraped. Exiting...")
            break

        preprocessed_thread, thread_ID = get_thread_Json(thread_ID)

        if not preprocessed_thread:
            print("Thread %d isn't available anymore" % thread_ID)
            break

        store_to_db(db,preprocessed_thread)

        if thread_counter % 50 == 0 and thread_counter > 0:
            print(thread_counter,flush=True)

        thread_counter += 1
        sleep(1.5 - time() % 1.5)


    db.close()

main()