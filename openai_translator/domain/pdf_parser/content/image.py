import os
from domain.pdf_parser.content.content import IMAGE_CONTENT, Content

IMAGE_SAVE_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../../images"))


class Image(Content):
    def __init__(self, raw_image_content):
        super().__init__(IMAGE_CONTENT)
        self.top = raw_image_content.get("top")
        self.original_name = raw_image_content.get("image_name")
        self.original = os.path.abspath(os.path.join(IMAGE_SAVE_DIR, self.original_name))
        self.width = raw_image_content.get("width")
        self.height = raw_image_content.get("height")

    def format_translation(self, translation):
        self.translation = translation
        self.is_translated = True

if __name__ == "__main__":
    print(IMAGE_SAVE_DIR)