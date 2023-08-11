import os
from flask import Flask, send_from_directory, abort, request
from service.translate_service import TranslateService

app = Flask(__name__)

@app.route('/translate', methods=['POST'])
def download():
    try:
        input_file_name = request.form.get('file_name')
        target_langunage = request.form.get('target_langunage')
        writer_format = request.form.get('writer_format')
        llm_model_name = request.form.get('llm_model_name')
        output_file_path = TranslateService.translate_pdf(input_file_name, target_langunage, writer_format, llm_model_name)
        folder = os.path.dirname(output_file_path)
        file_name = os.path.basename(output_file_path)
        return send_from_directory(folder, file_name, as_attachment=True)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    app.run()