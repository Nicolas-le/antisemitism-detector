from collections import defaultdict, Counter
from nltk.util import ngrams

def preprocess_post_per_time_interval(retrieval, time_interval):
    retrieved_data = retrieval.retrieve_detections_per_time_interval(time_interval)

    return retrieved_data


def get_keyword_information(retrieval, spacy_en_core, keyword_list):
    keyword_threads = get_thread_with_keywords(retrieval.restructured_data_set, keyword_list)
    keyword_coocs = get_coocs(spacy_en_core, keyword_threads, keyword_list)
    highest_cooc_words = get_highest_cooc_words(keyword_coocs)

    return highest_cooc_words


def get_thread_with_keywords(restructured_dataset, keyword_list):
    keyword_threads = []

    for thread_id, thread in restructured_dataset.items():
        if any([True for x in keyword_list if x in thread["initial_comment"]]):
            keyword_threads.append({thread_id: thread})
        else:
            continue

    return keyword_threads

def get_coocs(spacy_en_core, keyword_threads, keyword_list, include_replies=True):
    def remove_stopwords(words):
        all_stopwords = spacy_en_core.Defaults.stop_words
        tokens_without_sw = [word for word in words if not word in all_stopwords]
        punctuations = [".", ",", "-", "\"", ":", "?", "!", "\'","(",")","\'\'","@","//","","``","%"]
        tokens_without_sw = [word for word in tokens_without_sw if not word in punctuations]
        return tokens_without_sw

    def find_coocs(comment,n_gram_range,word):
        comment = remove_stopwords(comment)
        comment_n_grams = list(ngrams(comment, n_gram_range))

        coocs = []

        for gram in comment_n_grams:
            if gram[int(n_gram_range / 2)] == word:
                coocs.append(list(gram))
        return coocs

    keyword_coocs = defaultdict(list)

    for kw_thread in keyword_threads:

        for word in keyword_list:
            value, = kw_thread.values()
            coocs = find_coocs(value["initial_comment"], 9, word)
            if coocs:
                keyword_coocs[word].append(coocs)

            if include_replies:
                for reply in value["replies"]:
                    coocs = find_coocs(reply["comment"], 9, word)
                    if coocs:
                        keyword_coocs[word].append(coocs)

    return keyword_coocs

def get_highest_cooc_words(keyword_coocs):
    keyword_coocs_counts = defaultdict()
    highest_cooc_words = {}

    for keyword, coocs in keyword_coocs.items():
        keyword_dict = defaultdict(int)

        for cooc_list in coocs:
            for cooc in cooc_list:
                for word in cooc:
                    keyword_dict[word] += 1

        keyword_coocs_counts[keyword] = keyword_dict

        k = Counter(keyword_coocs_counts[keyword])
        high = k.most_common(11)

        highest_cooc_words[keyword] = high[1:]

    return highest_cooc_words