import os
from flask import Flask, render_template, request, send_file
from pdf2docx import Converter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'pdf_file' not in request.files:
            return 'No file part'
        file = request.files['pdf_file']
        if file.filename == '':
            return 'No selected file'
        
        if file:
            pdf_path = os.path.join(UPLOAD_FOLDER, file.filename)
            docx_filename = file.filename.rsplit('.', 1)[0] + '.docx'
            docx_path = os.path.join(UPLOAD_FOLDER, docx_filename)
            
            file.save(pdf_path)
            
            # แปลง PDF เป็น Word โดยรักษาเลย์เอาต์
            cv = Converter(pdf_path)
            cv.convert(docx_path, start=0, end=None)
            cv.close()
            
            return send_file(docx_path, as_attachment=True)
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)