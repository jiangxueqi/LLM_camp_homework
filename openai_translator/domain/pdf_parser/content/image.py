import os
from domain.pdf_parser.content.content import IMAGE_CONTENT, Content

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_DIR = os.path.abspath(os.path.join(CURR_DIR, "../../../images"))


class Image(Content):
    def __init__(self, raw_image_content):
        super().__init__(IMAGE_CONTENT)
        self._format_save_dir()
        self.content = None
        self.top = raw_image_content.get("top")
        self.image_path = os.path.abspath(os.path.join(SAVE_DIR, raw_image_content.get("image_name")))


if __name__ == "__main__":
    print(SAVE_DIR)