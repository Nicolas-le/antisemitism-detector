from tinydb import TinyDB, Query
import requests

db = TinyDB('4chan_pol_database.json')

antisem_list = ["jew","kike","zionist","israel","shylock","yid"]

antisem_threads = []
antisem_counter = 0

for i in db.all():
    if any([True for x in antisem_list if x in i["initial_comment"]]):
        antisem_threads.append(i)
    else:
        continue

for i in antisem_threads:
    #print(i["initial_comment"])
    antisem_counter += 1
    #antisem_counter += len(i["replies"])
    #print()
    for sub in i["replies"]:
        if any([True for x in antisem_list if x in sub["comment"]]):
            #print(sub["comment"])
            #print()
            antisem_counter += 1
    
    #print("\n\n\n")
    #print("#"*100)

print(antisem_counter)

        