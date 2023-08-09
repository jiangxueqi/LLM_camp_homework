import os
import pdfplumber

from domain.pdf_parser.content.image import SAVE_DIR
from domain.pdf_parser.content.table import Table
from domain.pdf_parser.content.text import Text


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
            pdf_page = pdf.pages[1]
            return self.parse_pdf_page(pdf_page)


    def parse_pdf_page(self, pdf_page):
        # text_contents = self.format_text_contets(pdf_page)
        # table_contents = self.format_table_contents(pdf_page)
        image_content = self.format_image_contents(pdf_page)

    def format_text_contets(self, pdf_page):
        text_contents = []
        raw_text_contents = self._format_raw_text_contents(pdf_page)
        if len(raw_text_contents) == 1:
            text_contents.append(Text(raw_text_contents[0]))
            return text_contents
        elif len(raw_text_contents) > 1:
            i, j = 0, 1
            while j <= len(raw_text_contents) - 1:
                if not self._is_belong_to_a_whole_text_content(raw_text_contents[i], raw_text_contents[j]):
                    whole_text_content = self._format_whole_text_content(raw_text_contents[i:j])
                    text_contents.append(Text(whole_text_content))
                    i = j
                j += 1
            whole_text_content = self._format_whole_text_content(raw_text_contents[i:])
            text_contents.append(Text(whole_text_content))
        return text_contents

    def _format_raw_text_contents(self, pdf_page):
        raw_text_lines = self._format_raw_text_lines(pdf_page)
        pure_raw_text_lines = self._format_pure_raw_text_lines(pdf_page)
        raw_text_contents = []
        for i in range(len(pure_raw_text_lines)):
            for j in range(len(raw_text_lines)):
                if pure_raw_text_lines[i].replace(" ", "") == raw_text_lines[j]["text"].replace(" ", ""):
                    raw_text_contents.append(raw_text_lines[j])
        return raw_text_contents

    def _is_belong_to_a_whole_text_content(self, raw_text_content_1, raw_text_content_2):
        return raw_text_content_1["fontname"] == raw_text_content_2["fontname"] and raw_text_content_1["size"] == raw_text_content_2["size"]

    def _format_whole_text_content(self, raw_text_contents):
        if len(raw_text_contents) == 1:
            return raw_text_contents[0]
        elif len(raw_text_contents) > 1:
            text = raw_text_contents[0].get("text")
            for i in range(1, len(raw_text_contents)):
                text += "\n{}".format(raw_text_contents[i]["text"])
            top = raw_text_contents[0].get("top")
            fontname = raw_text_contents[0].get("fontname")
            size = raw_text_contents[0].get("size")
            return {"text":text, "top":top, "fontname":fontname, "size":size}

    def _format_raw_text_lines(self, pdf_page):
        return [{"text":item.get("text"), "top":item.get("top"), "fontname":item.get("chars")[0].get("fontname"), "size":item.get("chars")[0].get("size")} for item in pdf_page.extract_text_lines(layout=True)]

    def _format_pure_raw_text_lines(self, pdf_page):
        raw_text = pdf_page.extract_text(layout=True)
        tables = pdf_page.extract_tables()
        for table_data in tables:
            for row in table_data:
                for cell in row:
                    raw_text = raw_text.replace(cell, "", 1)
        raw_text_lines = raw_text.splitlines()
        return [line.strip() for line in raw_text_lines if line.strip()]


    def format_table_contents(self, pdf_page):
        table_contents = []
        raw_table_contents = self._format_raw_table_contents(pdf_page)
        for raw_table in raw_table_contents:
            table_contents.append(Table(raw_table))
        return table_contents

    def _format_raw_table_contents(self, pdf_page):
        raw_table_contents = []
        raw_text_lines = self._format_raw_text_lines(pdf_page)
        raw_tables = pdf_page.extract_tables()
        tables_start_indexs = self._format_tables_start_indexs(raw_text_lines, raw_tables)
        for i ,j in enumerate(tables_start_indexs):
            table = raw_tables[i]
            top = raw_text_lines[j]["top"]
            head_fontname = raw_text_lines[j]["fontname"]
            head_size = raw_text_lines[j]["size"]
            body_fontname = raw_text_lines[j+1]["fontname"]
            body_size = raw_text_lines[j+1]["size"]
            raw_table_contents.append({"table":table, "top":top, "head_fontname":head_fontname, "head_size":head_size, "body_fontname":body_fontname, "body_size":body_size})
        return raw_table_contents

    def _format_tables_start_indexs(self, raw_text_lines, raw_tables):
        tables_start_index_list = []
        i, j = 0, 0
        while i <= len(raw_text_lines) - 1:
            if j <= len(raw_tables) - 1:
                if raw_text_lines[i]["text"].replace(" ", "") == "".join(raw_tables[j][0]).replace(" ", ""):
                    tables_start_index_list.append(i)
                    i += len(raw_tables[j])
                    j += 1
                else:
                    i += 1
            else:
                break
        return tables_start_index_list

    def format_image_contents(self, pdf_page):
        image_contents = []
        for index, img in enumerate(pdf_page.images):
            page_num = img["page_number"]
            top = img["top"]
            bbox = (img["x0"], img["top"], img["x1"], img["bottom"])
            cropped_page = pdf_page.crop(bbox)
            im = cropped_page.to_image(antialias=True)
            image_name = f"{page_num}_{index+1}.png"
            self._save_image(im, image_name)
            raw_image_content = {"image_name":image_name, "top":top}
            image_contents.append(raw_image_content)
        return image_contents

    def _save_image(self, im, image_name):
        if not os.path.exists(SAVE_DIR):
            os.mkdir(SAVE_DIR)
        image_path = os.path.abspath(os.path.join(SAVE_DIR, image_name))
        im.save(image_path)




if __name__ == "__main__":
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    test_pdf_path = os.path.abspath(os.path.join(curr_dir, "../../tests/test.pdf"))
    pdf = Pdf(test_pdf_path)
    pdf.parse_pdf()
