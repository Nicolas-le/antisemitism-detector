import pandas as pd

def get_keywords():
    """
    Keyword as dictionary. To filled by hand.
    """
    return  {

        "jewish": ["jew", "jews", "jewish", "judaism", "david","jewed","israeli","israelis","rabbi"],
        "middle_east": ["israel", "zionist", "zionists", "zionisti", "palestinian", "palestinians", "nationalist", "hamas", "idf",
                          "gaza","mossad"],
        "slurs": ["kike", "kikes", "shylock", "zog", "yid", "zhyd", "shyster", "smouch", "scapegoat", "grug","schlomo",
                     "jizzrael","jewsrael","jewmerica","israhell","jidf","globohomo","kikelover","hooknose","cryptojew",
                     "jewtube"],
        "racist": ["nigger", "niggers", "racist", "migrants"],
        "synonyms": ["bankers", "ngos", "interests", "globalist", "greed", "illuminati", "nwo", "academics",
                       "lobbyists","goldstein","shekelberg","sheklestien","rothschild"],
        "uncategorized": ["hitler", "holocaust", "whites", "sand", "nazi", "antisemitic", "clannish", "control",
                            "cowardice", "creatures", "(((echo)))", "silencing", "media","holohoax","(((media)))",
                             "(((their)))","(((journalist)))","(((lawyers)))","(((democracy)))","jewry","talmudvision",
                             "hollywoodcuckmuzzlei","yidtheatre","nuremberg","sidelock","shekel","shekels"]
    }

if __name__ == "__main__":
    """
    Create *.csv file from keyword dictionary in order to have a consistent list throughout multiple later uses of the list.
    """
    keyword_df = pd.DataFrame(columns=["category","keyword"])

    for category, keywords in get_keywords().items():
        for keyword in keywords:
            keyword_df  = keyword_df .append({"category": category,"keyword":keyword}, ignore_index=True)

    keyword_df.to_csv("../../keywords.csv")


