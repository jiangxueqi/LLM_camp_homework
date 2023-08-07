from domain.llm_model.llm_model import LLMModel

import openai

from infrastructure.utils.repeat import retries_on_exception


class OpenAIModel(LLMModel):
    def __init__(self, model_type, api_key):
        super().__init__()
        self.model_type = model_type
        openai.api_key = api_key


    def make_request(self, prompt):
        if "gpt-3.5" in self.model_type or "gpt-4" in self.model_type:
            message = self._format_translate_messages(prompt)
            result = self.chat_completion_api(message)
        else:
            result = self.completion_api(prompt)
        if result:
            return result.strip(), True
        return "", False


    def _format_translate_messages(self, prompt):
        messages = [{"role":"system", "content":"我希望你能担任翻译、拼写校对和修辞改进的角色。我会用任何语言和你交流，你会识别语言，将其翻译为优美的语言回答我。"},
                    {"role":"user", "content":f"{prompt}"}]
        return messages

    @retries_on_exception()
    def chat_completion_api(self, messages, functions=None, function_call_name=None):
        if functions:
            if function_call_name and function_call_name != "none":
                response = openai.ChatCompletion.create(
                    model=self.model_type,
                    messages=messages,
                    functions=functions,
                    function_call={"name": function_call_name}
                )
            elif function_call_name and function_call_name == "none":
                response = openai.ChatCompletion.create(
                    model=self.model_type,
                    messages=messages,
                    functions=functions,
                    function_call="none"
                )
            else:
                response = openai.ChatCompletion.create(
                    model=self.model_type,
                    messages=messages,
                    functions=functions
                )
        else:
            response = openai.ChatCompletion.create(
                model=self.model_type,
                messages=messages,
        )
        return response.choices[0].text

    @retries_on_exception()
    def completion_api(self, prompt):
        response = openai.Completion.create(
            model=self.model_type,
            prompt=prompt,
            temperature=0,
            max_tokens=2048
        )
        return response.choices[0].text

if __name__ == "__main__":
    model_type = "text-davinci-003"
    api_key = "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"
    openai_model = OpenAIModel(model_type, api_key)

    prompt = "请把下面这段话翻译为中文：To be or not to be, that is the question."
    result, is_translation = openai_model.make_request(prompt)
    if is_translation:
        print(result)