TEXT_CONTENT = "text"
TABLE_CONTENT = "table"
IMAGE_CONTENT = "image"

class Content(object):
    def __init__(self, type):
        self.type = type
        self.original = None
        self.translation = None
        self.is_translate = False