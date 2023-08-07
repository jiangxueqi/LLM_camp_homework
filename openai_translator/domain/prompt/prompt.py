

class Prompt(object):

    @staticmethod
    def format_text_translate_prompt(text, target_language):
        return f"请将下面一段话准确优美地翻译为{target_language}: {text}"

    @staticmethod
    def format_text_translate_messages(text, target_language):
        content = f"请将下面一段话翻译为{target_language}: {text}"
        messages = [{"role": "system",
                     "content": "我希望你能担任翻译、拼写校对和修辞改进的角色。我会用任何语言和你交流，你会识别语言，将其翻译为准确优美的语言回答我，不要写解释。"},
                    {"role": "user",
                     "content": content}]
        return messages