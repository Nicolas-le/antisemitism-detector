from io import StringIO
from html.parser import HTMLParser
import re
import nltk

def check_appending(tmp_dict):
    if tmp_dict["comment"]:
        return True
    else:
        return False


def clean_comment(text):
    if text:
        cleaned_html = remove_html(text)
        cleaned_numbers = ''.join([i for i in cleaned_html if not i.isdigit()])
        cleaned_links = re.sub(r"http\S+", "", cleaned_numbers)
        cleaned_links = cleaned_links.replace(">","")

        final = nltk.word_tokenize(cleaned_links)
        final = [item.lower() for item in final]
        
        return final
    else:
        return []

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def remove_html(text):
    s = MLStripper()
    s.feed(text)
    return s.get_data()