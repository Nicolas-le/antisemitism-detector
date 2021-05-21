from db_retrieve import DBRetrieval
from empath import Empath
from collections import defaultdict

def get_info_per_date(date,empath_lex):
    retrieval = DBRetrieval()
    posts_of_date = retrieval.get_post_per_day(date)

    date_info = {
        "date": date,
        "topic_distr": topic_signal_mod(posts_of_date,empath_lex),
        "keyword_distr": keyword_distr(posts_of_date),
        "countings": countings(posts_of_date)
    }

    return date_info

def topic_signal_mod(posts_of_date,empath_lex):

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

def keyword_distr(posts_of_date):

    keyword_list = ["jew","kike","zionist","israel","shylock","yid"]
    keyword_distribution = {
        "day": defaultdict(int),
        "highest_threads": {
            "id": 0,
            "keyword_counts": defaultdict(int)
        }
    }
    day_tokens = []

    for thread in posts_of_date:
        thread_tokens = []
        thread_tokens += thread["initial_comment"]

        for reply in thread["replies"]:
            thread_tokens += reply

        if not thread_tokens:
            continue

        day_tokens += thread_tokens

        for keyword in keyword_list:
            keyword_distribution["highest_threads"]["keyword_counts"][keyword] = thread_tokens.count(keyword)

    for keyword in keyword_list:
        keyword_distribution["day"][keyword] = day_tokens.count(keyword)

    return keyword_distribution

def countings(posts_of_date):

    countings = {
        "thread_general": {
            "count": 0,
            "replies": 0,
            "word_count_total": 0,
            "word_count_without_stopwords": 0,
        },
        "special_threads": {
            "long": 0, #id
            "high_keyword_count": 0 #id
        }
    }
    countings["thread_general"]["count"] = len(posts_of_date)

    for thread in posts_of_date:
        countings["thread_general"]["replies"] += len(thread["replies"])

    return countings

#date = "05/13/21"
#empath_lex = Empath()
#print(get_info_per_date(date,empath_lex))