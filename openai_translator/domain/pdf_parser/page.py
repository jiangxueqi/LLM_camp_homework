import pdfplumber

class Page(object):
    def __init__(self):
        self.content_list = []

    def add_contents(self, contents):
        for content in contents:
            self.content_list.append(content)




