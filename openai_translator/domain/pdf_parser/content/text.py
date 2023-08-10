from domain.pdf_parser.content.content import Content, TEXT_CONTENT


class Text(Content):
    def __init__(self, raw_text_content):
        super().__init__(TEXT_CONTENT)
        self.original = raw_text_content.get("text")
        self.top = raw_text_content.get("top")
        self.fontname = raw_text_content.get("fontname")
        self.size = raw_text_content.get("size")

    def format_translation(self, translation):
        self.translation = translation
        self.is_translated = True