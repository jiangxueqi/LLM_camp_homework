from domain.prompt.prompt import Prompt


class LLMModel(object):

    def make_translate_request(self, content, target_langunage):
        if content.type == "text":
            prompt = Prompt.format_text_translate_prompt(content.original, target_langunage)
            messages = Prompt.format_text_translate_messages(content.original, target_langunage)
        elif content.type == "table":
            pass
        return self.make_request(prompt, messages)

    def make_request(self, prompt="", messages=[]):
        raise NotImplementedError("子类必须实现 make_request 方法")