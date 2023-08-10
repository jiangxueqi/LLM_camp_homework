from domain.pdf_parser.content.content import TEXT_CONTENT, TABLE_CONTENT, IMAGE_CONTENT
from domain.prompt.prompt import Prompt


class LLMModel(object):

    def make_translate_request(self, content, target_langunage):
        if content.type == TEXT_CONTENT:
            prompt = Prompt.format_text_translate_prompt(content.original, target_langunage)
            messages = Prompt.format_text_translate_messages(content.original, target_langunage)
            return self.make_request(prompt, messages)
        elif content.type == TABLE_CONTENT:
            prompt = Prompt.format_table_translate_prompt(content.original, target_langunage)
            messages = Prompt.format_table_translate_messages(content.original, target_langunage)
            return self.make_request(prompt, messages)
        elif content.type == IMAGE_CONTENT:
            return content.original, True

    def make_request(self, prompt="", messages=[]):
        raise NotImplementedError("子类必须实现 make_request 方法")