
import os
import pdfplumber
from domain.pdf_parser.page import Page



class Pdf(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = None
        self.page_list = []
        self.parse_pdf()

    def parse_pdf(self):
        with pdfplumber.open(self.file_path) as pdf:
            self.metadata = pdf.metadata
            self.page_list = [Page(page_object) for page_object in pdf.pages]



if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    test_pdf_path = os.path.abspath(os.path.join(curr_dir, "../../tests/test.pdf"))
    pdf = Pdf(test_pdf_path)
    page1 = pdf.page_list[0]
    print(page1.text_lines[0])
    print(page1.text.split("\n"))
