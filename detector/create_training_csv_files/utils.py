

def delete_keywords(comment, keyword_list):
    comment = [word for word in comment if not word in keyword_list]
    return comment

def get_slur_keywords():
    kl_slurs = ["kike","kikes","shylock","zog","yid","zhyd","shyster","smouch","scapegoat","grug","schlomo","jizzrael","jewsrael","jewmerica","israhell","jidf"]
    kl_racist = ["nigger","niggers","racist","migrants"]

    keyword_list = kl_slurs + kl_racist
    return keyword_list

def get_all_keywords():
    kl_jewish = ["jew","jews","jewish","judaism","david"]
    kl_middle_east = ["israel","zionist","zionists","palestinian","palestinians","nationalist","hamas","idf","gaza"]
    kl_slurs = ["kike","kikes","shylock","zog","yid","zhyd","shyster","smouch","scapegoat","grug"]
    kl_racist = ["nigger","niggers","racist","migrants"]
    kl_synonyms = ["bankers","ngos","interests","globalist","greed","illuminati","nwo","academics","lobbyists"]
    kl_uncategorized = ["hitler","holocaust","whites","sand","nazi","antisemitic","clannish","control","cowardice","creatures","(((echo)))","silencing","media"]

    keyword_list = kl_jewish + kl_middle_east + kl_slurs + kl_racist + kl_synonyms + kl_uncategorized
    return keyword_list

