from tinydb import TinyDB

class Post():
    def __init__(self, comment, label):
        self.comment = self.remove_tokens(comment)
        self.label = "__label__" + self.convert_label(label)

    def remove_tokens(self, comment):
        return ' '.join(word for word in comment)

    def convert_label(self, label):
        if label == 1:
            return "antisemitic"
        if label == 0:
            return "notantisemitic"
        if label == 3:
            return "unsure"

def write_to_file(file, post):
    line = post.label + " " + post.comment + "\n"
    file.write(line)

def delete_keywords(comment):
    keyword_list = ["jew","jews","bankers","kike","hitler","kikes","nigger","niggers","holocaust","whites","racist","zionist","palestinian","palestinians","ngos","migrants","shylock","jewish","interests","nationalist","sand","zog","yid"]
    comment = [word for word in comment if not word in keyword_list]

    return comment

def iterate_file(without_keyword,file_name,db):
    with open(file_name, 'w') as file:
        if without_keyword:
            for entry in db.all():
                entry = dict(entry)
                for i in entry.items():
                    comment = delete_keywords(i[1]["comment"])
                    post = Post(comment,i[1]["label"])
                    write_to_file(file, post)
        else:
            for entry in db.all():
                entry = dict(entry)
                for i in entry.items():
                    post = Post(i[1]["comment"],i[1]["label"])
                    write_to_file(file, post)

def main():
    db = TinyDB('../data_set/antisemitic_subset.json')
    without_keyword = True

    if without_keyword:
        iterate_file(without_keyword,"data.train_without_keywords.txt",db)
    else:
        iterate_file(without_keyword,"data.train.txt",db)


main()