import os

from infrastructure.utils.yaml_load import load
CURR_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.abspath(os.path.join(CURR_DIR, "config.yaml"))

class ConfigLoader(object):

    @staticmethod
    def get_open_ai_model_name():
        return load(CONFIG_PATH).get("OpenAIModel").get("model")

    @staticmethod
    def get_open_ai_api_key():
        return load(CONFIG_PATH).get("OpenAIModel").get("api_key")

if __name__ == "__main__":
    print(ConfigLoader.get_open_ai_api_key())
