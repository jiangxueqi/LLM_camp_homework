from config.config_loader import ConfigLoader
from domain.llm_model.openai_model import OpenAIModel


class LLMModelFactory(object):

    def create(self, llm_model_name):
        if llm_model_name == "OpenAIModel":
            llm_model = self._create_open_ai_model()
        return llm_model


    def _create_open_ai_model(self):
        model_name = ConfigLoader.get_open_ai_model_name()
        api_key = ConfigLoader.get_open_ai_api_key()
        return OpenAIModel(model_name, api_key)