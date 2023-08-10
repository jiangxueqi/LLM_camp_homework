import os.path

from domain.pdf_parser.content.content import TEXT_CONTENT, TABLE_CONTENT, IMAGE_CONTENT
from domain.pdf_translator.writer.writer import Writer
from infrastructure.logger.logger import LOG
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, PageBreak


class PdfWriter(Writer):
    def __init__(self):
        super().__init__()
        self.output_file_suffix = ".pdf"

    def save_translation(self, pdf_parser, output_file_path):
        self.check_output_file_suffix(output_file_path)
        self._load_font("simsun.ttc")
        LOG.info(f"PDF开始翻译: {output_file_path}")
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
        story = self._format_story(pdf_parser)
        doc.build(story)
        LOG.info(f"PDF翻译完成: {output_file_path}")

    def _load_font(self, font_name):
        font_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../fonts/{font_name}"))
        pdfmetrics.registerFont(TTFont("SimSun", font_path))


    def _format_story(self, pdf_parser):
        story = []
        for page in pdf_parser.page_list:
            for content in page.content_list:
                para = self._format_para(content)
                story.append(para)
            if page != pdf_parser.page_list[-1]:
                story.append(PageBreak())
        return story

    def _format_para(self, content):
        if content.type == TEXT_CONTENT:
            return self._format_text_para(content)
        elif content.type == TABLE_CONTENT:
            return self._format_table_para(content)
        elif content.type == IMAGE_CONTENT:
            return self._format_image_para(content)


    def _format_text_para(self, content):
        text = content.translation
        fontname = "SimSun"
        size = int(content.size)
        font_style = self._format_font_style(fontname, size)
        return Paragraph(text, font_style)

    def _format_font_style(self, fontname, size):
        return ParagraphStyle(f'{fontname}', fontName=fontname, fontSize=size, leading=14)

    def _format_table_para(self, content):
        table_list = [content.translation.columns.tolist()] + content.translation.values.tolist()
        table_para = Table(table_list)
        table_style = self._format_table_style(content)
        table_para.setStyle(table_style)
        return table_para

    def _format_table_style(self, content):
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'SimSun'),  # 更改表头字体
            ('FONTSIZE', (0, 0), (-1, 0), int(content.head_size)),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('FONTNAME', (0, 1), (-1, -1), 'SimSun'),  # 更改表格中的字体
            ('GRID', (0, 0), (-1, -1), 1, int(content.body_size))
        ])

    def _format_image_para(self, content):
        image = Image(content.translation)
        image.drawWidth = content.width
        image.drawHeight = content.height
        return image

if __name__ == "__main__":
    font_name = "simsun.ttc"
    print(os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), f"../../../fonts/{font_name}")))


