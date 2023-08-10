from domain.pdf_translator.writer.markdown_writer import MarkdownWriter
from domain.pdf_translator.writer.pdf_writer import PdfWriter


class WriterFactory(object):

    def create(self, writer_format):
        if writer_format == "markdown":
            return MarkdownWriter()
        elif writer_format == "pdf":
            return PdfWriter()