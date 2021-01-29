from tinydb import TinyDB, Query
import requests

db = TinyDB('4chan_pol_database.json')

antisem_list = ["jew","kike","zionist","israel","palestine","shylock","yid"]

antisem_threads = []


for i in db.all():
    if any([True for x in antisem_list if x in i["initial_comment"]]):
        #print(i["initial_comment"])
        antisem_threads.append(i)

        #for sub in i["replies"]:
        #    print(sub["comment"])

        #print()
    else:
        continue

for i in antisem_threads[:1]:
    print(i["initial_comment"])
    
    for sub in i["replies"]:
        print(sub["comment"])