from domain.factory.llm_model_factory import LLMModelFactory
from domain.factory.writer_factory import WriterFactory
from domain.pdf_parser.pdf_parser import PdfParser


class Translator():
    def __init__(self, llm_model_name, writer_format):
        self.llm_model = LLMModelFactory().create(llm_model_name)
        self.writer = WriterFactory().create(writer_format)


    def translate(self, source_file_path, output_file_path, target_langunage):
        pdf_parser = PdfParser(source_file_path)
        for page in pdf_parser.page_list:
            for content in page.content_list:
                translation, is_ok = self.llm_model.make_translate_request(content, target_langunage)
                if is_ok:
                    content.format_translation(translation)
        self.writer.save_translation(pdf_parser, output_file_path)

if __name__ == "__main__":
    import os
    llm_model_name = "OpenAIModel"
    writer_format = "pdf"
    target_langunage = "中文"
    source_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../tests/test.pdf"))
    output_file_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../../tests/test_ZH.pdf"))
    Translator(llm_model_name, writer_format).translate(source_file_path, output_file_path, target_langunage)
