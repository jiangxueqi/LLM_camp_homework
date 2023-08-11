import os
from domain.pdf_translator.translator import Translator


class TranslateService(object):

    @staticmethod
    def translate_pdf(input_file_name, target_langunage, writer_format="pdf", llm_model_name="OpenAIModel"):
        input_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../file_input/{input_file_name}"))
        output_file_path = TranslateService._format_output_file_path(input_file_name, writer_format)
        Translator(llm_model_name, writer_format).translate(input_file_path, output_file_path, target_langunage)
        return output_file_path

    @staticmethod
    def _format_output_file_path(input_file_name, writer_format):
        input_file_name_without_extension = os.path.splitext(input_file_name)[0]
        out_file_extension = TranslateService._format_output_file_extension(writer_format)
        output_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../file_output/{input_file_name_without_extension}_translation{out_file_extension}"))
        return output_file_path

    @staticmethod
    def _format_output_file_extension(writer_format):
        if writer_format == "pdf":
            return ".pdf"
        elif writer_format == "markdown":
            return ".md"

if __name__ == "__main__":
    input_file_name = "test.pdf"
    target_langunage = "中文"
    writer_format = "markdown"
    TranslateService.translate_pdf(input_file_name, target_langunage, writer_format)
