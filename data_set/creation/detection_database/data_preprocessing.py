from data_set.creation.detection_database.db_retrieve import DBRetrieval
from collections import defaultdict

# initialize retrieval object for database connection
retrieval = DBRetrieval()

def get_info_per_date(date,empath_lex,spacy_en_core):
    """
    Main functionality for the analysis.
    """

    posts_of_date = retrieval.get_post_per_day(date)

    date_info = {
        "topic_distr": topic_signal_mod(posts_of_date,empath_lex),
        "keyword_distr": get_keyword_distr(posts_of_date),
        "countings": get_countings(posts_of_date,spacy_en_core)
    }

    return date_info

def topic_signal_mod(posts_of_date,empath_lex):
    """
    Returns the top ten topic for a specific date (time).
    """
    date_tokens = []

    # all the tokens of threads and posts are added to the whole date token list
    for thread in posts_of_date:
        date_tokens += thread["initial_comment"]
        for reply in thread["replies"]:
            date_tokens += reply

    # analyze the whole tokens of the date
    date_topics = empath_lex.analyze(date_tokens, normalize=True)

    # thresholöd for detected topics
    threshold = 0.001
    if date_topics is not None:
        date_topic_dictionary = {k: v for k,v in date_topics.items() if v >= threshold}
    else:
        return []

    date_topic_dictionary = {k: v for k, v in sorted(date_topic_dictionary.items(), key=lambda item: item[1], reverse=True)}
    top_ten = list(date_topic_dictionary.items())[2:12]

    return top_ten

def get_keyword_list():
    """
    Reduced keyword list, that's why the csv isn't used.
    """
    # keyword_list = ["jew", "kike", "zionist", "israel", "shylock", "yid"] old one

    kl_jewish = ["jew", "jews", "jewish", "judaism", "david"]
    kl_middle_east = ["israel", "zionist", "zionists", "palestinian", "palestinians", "nationalist", "hamas", "idf",
                      "gaza"]
    kl_slurs = ["kike", "kikes", "shylock", "zog", "yid", "zhyd", "shyster", "smouch", "scapegoat", "grug"]
    kl_racist = ["nigger", "niggers", "racist", "migrants"]
    kl_synonyms = ["bankers", "ngos", "interests", "globalist", "greed", "illuminati", "nwo", "academics", "lobbyists"]
    kl_uncategorized = ["hitler", "holocaust", "whites", "sand", "nazi", "antisemitic", "clannish", "control", "cowardice",
               "creatures", "(((echo)))", "silencing", "media"]

    final_list = kl_jewish + kl_middle_east + kl_slurs + kl_racist + kl_synonyms + kl_uncategorized

    return final_list

def get_keyword_distr(posts_of_date):
    """
    Returns a dictionary containing the threads with the highest keyword_counts and their distribution.
    """
    keyword_list = get_keyword_list()

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
    """
    Get all the counting information.
    """
    # dictionary structure for the countings
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

    # first counting: post count
    countings["thread_general"]["count"] = len(posts_of_date)

    for thread in posts_of_date:
        # count the total number of replies
        countings["thread_general"]["replies"] += len(thread["replies"])
        all_words += thread["initial_comment"]
        for reply in thread["replies"]:
            all_words += reply

        # save thread IDs with a reply count over 10
        if len(thread["replies"]) > 10:
            countings["special_threads"]["traffic"].append((thread["thread"],len(thread["replies"])))

    # word counts total and without stopwords
    countings["thread_general"]["word_count_total"] = len(all_words)
    countings["thread_general"]["word_count_without_stopwords"] = len(remove_stopwords(sp,all_words))
    return countings

def remove_stopwords(sp, words):
    all_stopwords = sp.Defaults.stop_words
    tokens_without_sw = [word for word in words if not word in all_stopwords]
    return tokens_without_sw

def get_dates(time_interval):
    """
    Returns all the dates in the dataset in hourly or daily steps
    """
    dates = []
    if time_interval == "hourly":
        date_cut_length = 15
    else:
        date_cut_length = 13

    for thread in retrieval.get_db_all():
        dates.append(thread["posting_time"][:date_cut_length])

    return list(dict.fromkeys(dates))
