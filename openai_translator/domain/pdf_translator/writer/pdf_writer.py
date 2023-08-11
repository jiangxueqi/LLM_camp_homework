import os.path

from config.config_loader import ConfigLoader
from domain.pdf_parser.content.content import TEXT_CONTENT, TABLE_CONTENT, IMAGE_CONTENT
from domain.pdf_translator.writer.writer import Writer
from infrastructure.logger.logger import LOG
from reportlab.lib import colors, pagesizes
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Image, PageBreak, Spacer

CURR_DIR = os.path.abspath(__file__)
FONTS_DIR = os.path.abspath(os.path.join(CURR_DIR, "../../../../fonts"))

COLOR_MAP = {"grey": colors.grey, "whitesmoke": colors.whitesmoke, "black":colors.black}

class PdfWriter(Writer):
    def __init__(self):
        super().__init__()
        self.output_file_suffix = ".pdf"

    def save_translation(self, pdf_parser, output_file_path):
        self.check_output_file_suffix(output_file_path)
        self._register_font()
        LOG.info(f"PDF开始翻译: {output_file_path}")
        doc = SimpleDocTemplate(output_file_path, pagesize=pagesizes.letter)
        story = self._format_story(pdf_parser)
        doc.build(story)
        LOG.info(f"PDF翻译完成: {output_file_path}")

    def _register_font(self):
        for font_name in os.listdir(FONTS_DIR):
            font_name_without_extension = os.path.splitext(font_name)[0]
            config_font_name = ConfigLoader.get_pdf_font_name()
            if config_font_name.lower() == font_name_without_extension.lower():
                font_path = os.path.abspath(os.path.join(FONTS_DIR, f"{font_name}"))
                pdfmetrics.registerFont(TTFont(config_font_name, font_path))

    def _format_story(self, pdf_parser):
        story = []
        for page in pdf_parser.page_list:
            for content in page.content_list:
                para = self._format_para(content)
                story.append(para)
                if content != page.content_list[-1]:
                    space_style = self._format_space_style()
                    story.append(space_style)
            if page != pdf_parser.page_list[-1]:
                story.append(PageBreak())
        return story

    def _format_space_style(self):
        space = ConfigLoader.get_pdf_space()
        return Spacer(1, space)

    def _format_para(self, content):
        if content.type == TEXT_CONTENT:
            return self._format_text_para(content)
        elif content.type == TABLE_CONTENT:
            return self._format_table_para(content)
        elif content.type == IMAGE_CONTENT:
            return self._format_image_para(content)

    def _format_text_para(self, content):
        text = content.translation
        font_style = self._format_font_style(content)
        return Paragraph(text, font_style)

    def _format_font_style(self, content):
        font_name = ConfigLoader.get_pdf_font_name()
        font_size = int(content.size)
        leading = ConfigLoader.get_pdf_text_leading()
        space_before = ConfigLoader.get_pdf_space_before()
        space_after = ConfigLoader.get_pdf_space_after()
        return ParagraphStyle(f'{font_name}', fontName=font_name, fontSize=font_size, leading=leading, spaceBefore=space_before, spaceAfter=space_after)

    def _format_table_para(self, content):
        table_list = [content.translation.columns.tolist()] + content.translation.values.tolist()
        table_para = Table(table_list)
        table_style = self._format_table_style(content)
        table_para.setStyle(table_style)
        return table_para

    def _format_table_style(self, content):
        head_background_color = ConfigLoader.get_pdf_table_head_background_color()
        head_text_color = ConfigLoader.get_pdf_table_head_text_color
        font_name= ConfigLoader.get_pdf_font_name()
        grid_colors= ConfigLoader.get_pdf_table_grid_color()
        return TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), COLOR_MAP.get(head_background_color)),              # 设置表头背景颜色
            ('TEXTCOLOR', (0, 0), (-1, 0), COLOR_MAP.get(head_text_color)),                     # 设置表头文字颜色
            ('FONTNAME', (0, 0), (-1, 0), font_name),                                           # 设置表头字体
            ('FONTSIZE', (0, 0), (-1, 0), int(content.head_size)),                              # 设置表头字体大小
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),                                     # 设置表身背景颜色
            ('FONTNAME', (0, 1), (-1, -1), font_name),                                          # 设置表身的字体
            ('FONTSIZE', (0, 0), (-1, -1), int(content.body_size)),                             # 设置表身大小
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),                                              # 设置所有单元格居中对齐
            ('GRID', (0, 0), (-1, -1), 1, COLOR_MAP.get(grid_colors))                           # 设置表格线段颜色
        ])

    def _format_image_para(self, content):
        image = Image(content.translation)
        image.drawWidth = content.width
        image.drawHeight = content.height
        return image

if __name__ == "__main__":
    print(FONTS_DIR)
    print(os.path.exists(FONTS_DIR))


