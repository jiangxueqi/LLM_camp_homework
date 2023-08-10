import pandas as pd
from domain.pdf_parser.content.content import Content, TABLE_CONTENT


class Table(Content):
    def __init__(self, raw_table_content):
        super().__init__(TABLE_CONTENT)
        self.original_pd = self._format_pd(raw_table_content.get("table"))
        self.original = [self.original_pd.columns.tolist()] + self.original_pd.values.tolist()
        self.top = raw_table_content.get("top")
        self.head_fontname = raw_table_content.get("head_fontname")
        self.head_size = raw_table_content.get("head_size")
        self.body_fontname = raw_table_content.get("body_fontname")
        self.body_size = raw_table_content.get("body_size")


    def _format_pd(self, table_lists):
        return pd.DataFrame(table_lists[1:], columns=table_lists[0], index=None)

    def format_translation(self, translation):
        self.translation = self._format_pd(eval(translation))
        self.is_translated = True


if __name__ == "__main__":
    _str = "[[1,2],[3,4]]"
    print(eval(_str))