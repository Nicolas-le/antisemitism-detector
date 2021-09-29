class Post():
    def __init__(self, comment, label):
        self.comment = self.remove_tokens(comment)
        self.label = label

    def remove_tokens(self, comment):
        return ' '.join(word for word in comment)

