

class Prompt(object):

    @staticmethod
    def format_text_translate_prompt(text, target_language):
        return f"请将下面一段话准确优美地翻译为{target_language}: {text}"

    @staticmethod
    def format_text_translate_messages(text, target_language):
        content = f"请将下面一段话翻译为{target_language}: {text}"
        messages = [{"role": "system",
                     "content": "我希望你能担任翻译、拼写校对和修辞改进的角色。我会用任何语言和你交流，你会识别语言，将其翻译为准确优美的语言回答我，不要写解释。注意保留原有格式。"},
                    {"role": "user",
                     "content": content}]
        return messages

    @staticmethod
    def format_table_translate_prompt(table, target_language):
        return f"请将二维列表中的内容翻译为{target_language}，二维列表：{table}"

    @staticmethod
    def format_table_translate_messages(table, target_language):
        content = f"请将二维列表中的内容翻译为{target_language}，二维列表：{table}"
        messages = [{"role": "system",
                     "content": "我希望你能担任翻译、拼写校对和修辞改进的角色。我会用任何语言和你交流，你会识别语言，将其翻译为准确优美的语言回答我,结 果以二维列表的形式返回"},
                    {"role": "user",
                     "content": content}]
        return messages