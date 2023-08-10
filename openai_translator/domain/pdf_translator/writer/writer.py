import os

from infrastructure.logger.logger import LOG


class Writer(object):
    def __init__(self):
        self.output_file_suffix = None

    def save_translation(self, pdf_parser, output_file_path):
        raise NotImplementedError("子类必须实现 save_translation 方法")

    def check_output_file_suffix(self, output_file_path):
        file_extension = os.path.splitext(output_file_path)[1]
        if file_extension != self.output_file_suffix:
            error_info = f'保存文件的格式错误！不是"{file_extension}"，应是"{self.output_file_suffix}"'
            LOG.error(error_info)
            raise ValueError(error_info)

    def remove_output_file(self, output_file_path):
        if os.path.exists(output_file_path):
            os.remove(output_file_path)

