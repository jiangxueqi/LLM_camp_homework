import os
import pdfplumber



class Pdf(object):
    def __init__(self, file_path):
        self.file_path = file_path
        self.metadata = None


    def parse_pdf(self):
        with pdfplumber.open(self.file_path) as pdf:
            self.metadata = pdf.metadata
            # pdf_page = pdf.pages[0]
            # for pdf_page in pdf.pages:
            #     pass
            pdf_page = pdf.pages[0]
            return self.parse_pdf_page(pdf_page)


    def parse_pdf_page(self, pdf_page):
        result = []
        for item in pdf_page.extract_text_lines(layout=True):
            result.append(item.get("text"))
        return result


    # def _format_rects(self, pdf_page):
    #     return pdf_page.objects.get("rects")



if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    test_pdf_path = os.path.abspath(os.path.join(curr_dir, "../../tests/test.pdf"))
    pdf = Pdf(test_pdf_path)
    result = pdf.parse_pdf()
    print(result)
