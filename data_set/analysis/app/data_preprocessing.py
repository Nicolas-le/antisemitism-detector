from db_retrieve import DBRetrieval
from empath import Empath
from collections import defaultdict
import spacy

def get_info_per_date(date,empath_lex,spacy_en_core):
    retrieval = DBRetrieval()
    posts_of_date = retrieval.get_post_per_day(date)

    date_info = {
        "date": date,
        "topic_distr": topic_signal_mod(posts_of_date,empath_lex),
        "keyword_distr": get_keyword_distr(posts_of_date),
        "countings": get_countings(posts_of_date,spacy_en_core)
    }

    return date_info

def topic_signal_mod(posts_of_date,empath_lex):
    """
    Returns the top ten topic for a specific date (time).
    :param posts_of_date:
    :param empath_lex:
    :return:
    """

    date_topics = defaultdict(float)

    for thread in posts_of_date:
        thread_tokens = []
        thread_tokens += thread["initial_comment"]

        for reply in thread["replies"]:
            thread_tokens += reply

        if not thread_tokens:
            continue

        topics = empath_lex.analyze(thread_tokens, normalize=True)

        threshold = 0.001
        filtered_topics = {k: v for k,v in topics.items() if v >= threshold}

        for topic in filtered_topics:
            date_topics[topic] += filtered_topics[topic]

    date_topics = { k: v for k, v in sorted(date_topics.items(), key=lambda item: item[1], reverse=True) }
    top_ten = list(date_topics.items())[2:12]

    return top_ten

def get_keyword_distr(posts_of_date):
    """
    Returns a dictionary containing the threads with the highest keyword_counts and their distribution.
    :param posts_of_date:
    :return:
    """

    keyword_list = ["jew","kike","zionist","israel","shylock","yid"]
    keyword_distribution = {
        "percentage_of_keyword_occ": 0,
        "highest_threads": defaultdict(dict)
    }

    thread_with_keyword_count = 0
    # for every thread in retrieved posts from specific date
    for thread in posts_of_date:
        # collect tokens of initial comment and replies in one list
        thread_tokens = []
        thread_tokens += thread["initial_comment"]

        for reply in thread["replies"]:
            thread_tokens += reply

        # if there are no tokens found continue
        if not thread_tokens:
            continue

        # if there are 5 or more occurrences of keywords in thread, the thread is saved with counts to the dictionary
        count = 0
        tmp_dict = defaultdict(int)
        for keyword in keyword_list:
            keyword_count = thread_tokens.count(keyword)
            tmp_dict[keyword] = keyword_count
            count += keyword_count

        if count >= 3:
            keyword_distribution["highest_threads"][thread["thread"]] = tmp_dict

        if count > 0:
            thread_with_keyword_count += count

    # which percentage of posts contains at least one keyword
    keyword_distribution["percentage_of_keyword_occ"] = round(thread_with_keyword_count/len(posts_of_date),3)

    return keyword_distribution

def get_countings(posts_of_date, sp):

    countings = {
        "thread_general": {
            "count": 0,
            "replies": 0,
            "word_count_total": 0,
            "word_count_without_stopwords": 0,
        },
        "special_threads": {
            "traffic": [], #id
        }
    }
    all_words = []

    countings["thread_general"]["count"] = len(posts_of_date)

    for thread in posts_of_date:
        countings["thread_general"]["replies"] += len(thread["replies"])
        all_words += thread["initial_comment"]
        for reply in thread["replies"]:
            all_words += reply

        if len(thread["replies"]) > 10:
            countings["special_threads"]["traffic"].append((thread["thread"],len(thread["replies"])))

    countings["thread_general"]["word_count_total"] = len(all_words)
    countings["thread_general"]["word_count_without_stopwords"] = len(remove_stopwords(sp,all_words))

    return countings

def remove_stopwords(sp, words):
    all_stopwords = sp.Defaults.stop_words
    tokens_without_sw = [word for word in words if not word in all_stopwords]
    return tokens_without_sw

def get_thread(id):
    """
    Get specific thread to visualize
    :param id:
    :return:
    """

    return False

date = '05/12/21(Wed)05'

empath_lex = Empath()
spacy_en_core = spacy.load('en_core_web_sm')

date_info = get_info_per_date(date, empath_lex, spacy_en_core)
print(date_info)

#
#print(get_info_per_date(date,empath_lex))
"""
dates = ['05/12/21(Wed)06', '05/12/21(Wed)05', '05/12/21(Wed)04', '05/12/21(Wed)03', '05/12/21(Wed)02', '05/12/21(Wed)01', '05/12/21(Wed)00', '05/11/21(Tue)23', '05/11/21(Tue)22', '05/11/21(Tue)21', '05/11/21(Tue)20', '05/11/21(Tue)19', '05/11/21(Tue)18', '05/11/21(Tue)17', '05/11/21(Tue)16', '05/11/21(Tue)15', '05/11/21(Tue)14', '05/11/21(Tue)13', '05/11/21(Tue)12', '05/11/21(Tue)10', '05/11/21(Tue)11', '05/11/21(Tue)09', '05/11/21(Tue)00', '05/11/21(Tue)08', '05/11/21(Tue)07', '05/11/21(Tue)04', '05/11/21(Tue)06', '05/11/21(Tue)05', '05/11/21(Tue)02', '05/11/21(Tue)03', '05/11/21(Tue)01', '05/10/21(Mon)19', '05/10/21(Mon)23', '05/10/21(Mon)12', '05/10/21(Mon)22', '05/10/21(Mon)21', '05/10/21(Mon)20', '05/10/21(Mon)18', '05/10/21(Mon)17', '05/10/21(Mon)16', '05/10/21(Mon)15', '05/10/21(Mon)14', '05/10/21(Mon)13', '05/10/21(Mon)11', '05/10/21(Mon)10', '05/10/21(Mon)09', '05/10/21(Mon)08', '05/10/21(Mon)07', '05/10/21(Mon)06', '05/10/21(Mon)05', '05/10/21(Mon)04', '05/10/21(Mon)03', '05/10/21(Mon)02', '05/09/21(Sun)23', '05/10/21(Mon)01', '05/10/21(Mon)00', '05/09/21(Sun)22', '05/09/21(Sun)21', '05/09/21(Sun)20', '05/09/21(Sun)19', '05/09/21(Sun)18', '05/09/21(Sun)17', '05/09/21(Sun)16', '05/09/21(Sun)15', '05/09/21(Sun)14', '05/09/21(Sun)13', '05/09/21(Sun)12', '05/09/21(Sun)11', '05/09/21(Sun)10', '05/13/21(Thu)05', '05/13/21(Thu)04', '05/13/21(Thu)03', '05/13/21(Thu)02', '05/13/21(Thu)01', '05/13/21(Thu)00', '05/12/21(Wed)23', '05/12/21(Wed)15', '05/12/21(Wed)22', '05/12/21(Wed)21', '05/12/21(Wed)20', '05/12/21(Wed)19', '05/07/21(Fri)14', '05/12/21(Wed)18', '05/12/21(Wed)17', '05/12/21(Wed)16', '05/12/21(Wed)14', '05/12/21(Wed)13', '05/12/21(Wed)12', '05/12/21(Wed)10', '05/12/21(Wed)11', '05/12/21(Wed)09', '05/12/21(Wed)08', '05/12/21(Wed)07', '05/17/21(Mon)03', '05/17/21(Mon)02', '05/17/21(Mon)01', '05/17/21(Mon)00', '05/16/21(Sun)23', '05/16/21(Sun)22', '05/16/21(Sun)21', '05/16/21(Sun)20', '05/16/21(Sun)19', '05/16/21(Sun)18', '05/16/21(Sun)17', '05/16/21(Sun)16', '05/16/21(Sun)15', '05/16/21(Sun)14', '05/16/21(Sun)13', '05/16/21(Sun)12', '05/16/21(Sun)11', '05/16/21(Sun)10', '05/16/21(Sun)09', '05/16/21(Sun)08', '05/16/21(Sun)07', '05/16/21(Sun)06', '05/16/21(Sun)05', '05/16/21(Sun)04', '05/16/21(Sun)03', '05/16/21(Sun)02', '05/16/21(Sun)01', '05/16/21(Sun)00', '05/15/21(Sat)23', '05/15/21(Sat)22', '05/15/21(Sat)21', '05/15/21(Sat)20', '05/15/21(Sat)19', '05/15/21(Sat)18', '05/15/21(Sat)17', '05/15/21(Sat)16', '05/15/21(Sat)15', '05/15/21(Sat)14', '05/15/21(Sat)13', '05/15/21(Sat)12']
empath_lex = Empath()

all_distr = defaultdict(str)
for date in dates:
    all_distr[date] = get_info_per_date(date,empath_lex)


with open('all_distr.csv', 'w') as f:
    for key in all_distr.keys():
        f.write("%s,%s\n"%(key,all_distr[key]))
"""