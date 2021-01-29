import requests
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
    thread_json = requests.get("https://a.4cdn.org/pol/thread/"+str(thread_ID)+".json").json()
    return preprocess_json(thread_json)

def preprocess_json(thread_json):
    def handle_replies(posts):
        output_list = []
        for post in posts:
            tmp_dict = {
                "country": post["country_name"],
                "posting_time": post["now"],
                "comment": data_cleaner.clean_comment(post.get("com"))
            }
            
            if data_cleaner.check_appending(tmp_dict):
                output_list.append(tmp_dict)
            else:
                continue

        return output_list
    
    #with open('304255810.json') as thread_IDs_file:
    #    thread_json = json.load(thread_IDs_file)

    preprocessed_json = {
        "thread": thread_json["posts"][0]["no"],
        "initial_country": thread_json["posts"][0]["country_name"],
        "posting_time": thread_json["posts"][0]["now"],
        "initial_comment": data_cleaner.clean_comment(thread_json["posts"][0].get("com")),
        "replies": handle_replies(thread_json["posts"][1:]) # give handle_replies() all the following posts after initial post
    }

    return preprocessed_json

def store_to_db(db, preprocessed_json):
    db.insert(preprocessed_json)

def main():
    db = TinyDB('4chan_pol_database.json', storage=CachingMiddleware(JSONStorage))
    thread_IDs = get_IDs()

    save_counter = 0
    for thread_ID in thread_IDs[:5]:
        preprocessed_thread = get_thread_Json(thread_ID)
        store_to_db(db,preprocessed_thread)

        thread_IDs.remove(thread_ID)
        if save_counter % 500 == 0:
            filename = "./archive_ids_saves/save_point_" + str(save_counter) + ".json"
            with open(filename, 'w') as f:
                json.dump(thread_IDs, f)       

        sleep(1.5 - time() % 1.5)
        print(thread_ID,flush="True")

    db.close()

main()