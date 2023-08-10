from domain.pdf_parser.content.content import TEXT_CONTENT, TABLE_CONTENT, IMAGE_CONTENT
from domain.pdf_translator.writer.writer import Writer
from infrastructure.logger.logger import LOG


class MarkdownWriter(Writer):
    def __init__(self):
        super().__init__()
        self.output_file_suffix = ".md"

    def save_translation(self, pdf_parser, output_file_path):
        self.check_output_file_suffix(output_file_path)
        LOG.info(f"Markdown开始翻译: {output_file_path}")
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            for page in pdf_parser.page_list:
                for content in page.content_list:
                    self.save_content(output_file, content)
                if page != pdf_parser.page_list[-1]:
                    output_file.write('---\n\n')
        LOG.info(f"Markdown翻译完成: {output_file_path}")

    def save_content(self, output_file, content):
        if content.type == TEXT_CONTENT:
            self._save_text_content(output_file, content)
        elif content.type == TABLE_CONTENT:
            self._save_table_content(output_file, content)
        elif content.type == IMAGE_CONTENT:
            self._save_image_content(output_file, content)


    def _save_text_content(self, output_file, content):
        if content.is_translated:
            result = content.translation
        else:
            result = "Text翻译过程出现错误！"
        output_file.write(result + "\n\n")

    def _save_table_content(self, output_file, content):
        if content.is_translated:
            result = content.translation.to_markdown(index=False)
        else:
            result = "Table翻译过程出现错误！"
        output_file.write(result + "\n\n")

    def _save_image_content(self, output_file, content):
        if content.is_translated:
            result = f'![{content.original_name}]({content.original})'
        else:
            result = "Image翻译过程出现错误！"
        output_file.write(result + "\n\n")

