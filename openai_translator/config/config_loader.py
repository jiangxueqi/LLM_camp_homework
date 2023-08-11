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
    @staticmethod
    def get_pdf_font_name():
        return load(CONFIG_PATH).get("PDF_STYLE").get("font_name")
    @staticmethod
    def get_pdf_space():
        return load(CONFIG_PATH).get("PDF_STYLE").get("space")

    @staticmethod
    def get_pdf_text_leading():
        return load(CONFIG_PATH).get("PDF_STYLE").get("text_style").get("leading")

    @staticmethod
    def get_pdf_table_head_background_color():
        return load(CONFIG_PATH).get("PDF_STYLE").get("table_style").get("head_background_color")

    @staticmethod
    def get_pdf_table_head_text_color():
        return load(CONFIG_PATH).get("PDF_STYLE").get("table_style").get("head_text_color")

    @staticmethod
    def get_pdf_table_body_background_color():
        return load(CONFIG_PATH).get("PDF_STYLE").get("table_style").get("body_background_color")

    @staticmethod
    def get_pdf_table_grid_color():
        return load(CONFIG_PATH).get("PDF_STYLE").get("grid_color")

    @staticmethod
    def get_pdf_space_before():
        return load(CONFIG_PATH).get("PDF_STYLE").get("space_before")

    @staticmethod
    def get_pdf_space_after():
        return load(CONFIG_PATH).get("PDF_STYLE").get("space_after")



if __name__ == "__main__":
    print(ConfigLoader.get_pdf_table_head_background())
