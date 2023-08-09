import pandas as pd
from domain.pdf_parser.content.content import Content, TABLE_CONTENT


class Table(Content):
    def __init__(self, raw_table_content):
        super().__init__(TABLE_CONTENT)
        self.content = self._format_content(raw_table_content.get("table"))
        self.top = raw_table_content.get("top")
        self.head_fontname = raw_table_content.get("head_fontname")
        self.head_size = raw_table_content.get("head_size")
        self.body_fontname = raw_table_content.get("body_fontname")
        self.body_size = raw_table_content.get("body_size")


    def _format_content(self, table):
        return pd.DataFrame(table[1:], columns=table[0])