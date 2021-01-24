import requests
import json
from tinydb import TinyDB, Query
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
from tinydb.operations import add, delete
from io import StringIO
from html.parser import HTMLParser
from time import time, sleep
import re


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
                "comment": clean_comment(post.get("com"))
            }
            print(tmp_dict,flush=True)
            output_list.append(tmp_dict)

        return output_list
    
    #with open('304255810.json') as thread_IDs_file:
    #    thread_json = json.load(thread_IDs_file)

    preprocessed_json = {
        "thread": thread_json["posts"][0]["no"],
        "initial_country": thread_json["posts"][0]["country_name"],
        "posting_time": thread_json["posts"][0]["now"],
        "initial_comment": clean_comment(thread_json["posts"][0].get("com")),
        "replies": handle_replies(thread_json["posts"][1:]) # give handle_replies() all the following posts after initial post
    }

    print(preprocessed_json)
    return preprocessed_json

def clean_comment(text):
    if text:
        cleaned_html = remove_html(text)
        cleaned_numbers = ''.join([i for i in cleaned_html if not i.isdigit()])
        cleaned_links = re.sub(r'^https?:\/\/.*[\r\n]*', '', cleaned_numbers, flags=re.MULTILINE)
        return cleaned_links
    else:
        return ""

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def remove_html(text):
    s = MLStripper()
    s.feed(text)
    return s.get_data()

def store_to_db(db, preprocessed_json):
    db.insert(preprocessed_json)
    # save json to tinydb

def main():
    db = TinyDB('4chan_pol_database.json', storage=CachingMiddleware(JSONStorage))
    thread_IDs = get_IDs()

    # repeat every second
    for thread_ID in thread_IDs[:1]:
        preprocessed_thread = get_thread_Json(thread_ID)
        #store_to_db(preprocessed_json)
        sleep(10 - time() % 10)

        print(thread_ID,flush="True")


    # save json to tinydb


main()


