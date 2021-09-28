from pyfiglet import Figlet

def print_header(retrieval):
    f = Figlet(font="slant")
    print(f.renderText("Label Antisemitism"))
    print("Label the shit out of the comments!")
    antisem = 0
    nantisem = 0
    unsure = 0

    for comment in retrieval.antisemitic_subset.all():
        for id in comment:
            if comment[id]["label"] == 1:
                antisem += 1
            elif comment[id]["label"] == 0:
                nantisem += 1
            elif comment[id]["label"] == 3:
                unsure += 1

    print("The Database contains...\n...comments, "
          "labeled as antisemitic: {}\n...comments, labeled as not antisemitic: "
          "{}\n...and comments, labeled as unsure: {}".format(antisem, nantisem, unsure))
    print("_" * 100)

def create_keywords():
    kl_jewish = ["jew","jews","jewish","judaism","david"]
    kl_middle_east = ["israel","zionist","zionists","palestinian","palestinians","nationalist","hamas","idf","gaza"]
    kl_slurs = ["kike","kikes","shylock","zog","yid","zhyd","shyster","smouch","scapegoat","grug"]
    kl_racist = ["nigger","niggers","racist","migrants"]
    kl_synonyms = ["bankers","ngos","interests","globalist","greed","illuminati","nwo","academics","lobbyists"]
    kl_uncategorized = ["hitler","holocaust","whites","sand","nazi","antisemitic","clannish","control","cowardice","creatures","(((echo)))","silencing","media"]

    return kl_jewish + kl_middle_east + kl_slurs + kl_racist + kl_synonyms + kl_uncategorized

def make_decision():
    print("\n1 = antisem ; 0 = not antisem, 3 = unsure, 5 = break",flush=True)

    try:
        decision = int(input())
    except ValueError:
        print("No valid decision")
        return 5

    return decision