import pdfplumber

class Page(object):
    def __init__(self, pdf_page):
        self.pdf_page = pdf_page
        self.text_contents = []
        self.table_contents = []
        self.image_contents = []
        self.parser_page_content()

    @property
    def number(self):
        return self.pdf_page.page_number

    @property
    def width(self):
        return self.pdf_page.width

    @property
    def height(self):
        return self.pdf_page.height

    def parser_page_content(self):
        pass

