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
        raw_text_lines = self._format_raw_text_lines(pdf_page)
        cleaned_raw_text_lines = self._format_cleaned_raw_text_lines(pdf_page)
        print(raw_text_lines)
        print(cleaned_raw_text_lines)

    def _format_raw_text_lines(self, pdf_page):
        return pdf_page.extract_text_lines()[1]
        # return [item.get("text") for item in pdf_page.extract_text_lines()]

    def _format_cleaned_raw_text_lines(self, pdf_page):
        raw_text = pdf_page.extract_text()
        tables = pdf_page.extract_tables()
        for table_data in tables:
            for row in table_data:
                for cell in row:
                    raw_text = raw_text.replace(cell, "", 1)
        raw_text_lines = raw_text.splitlines()
        return [line.strip() for line in raw_text_lines if line.strip()]




if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    test_pdf_path = os.path.abspath(os.path.join(curr_dir, "../../tests/test.pdf"))
    pdf = Pdf(test_pdf_path)
    pdf.parse_pdf()
