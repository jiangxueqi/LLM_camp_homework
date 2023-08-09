from domain.pdf_parser.content.content import Content, TEXT_CONTENT


class Text(Content):
    def __init__(self, raw_text_content):
        super().__init__(TEXT_CONTENT)
        self.content = raw_text_content.get("text")
        self.top = raw_text_content.get("top")
        self.fontname = raw_text_content.get("fontname")
        self.size = raw_text_content.get("size")