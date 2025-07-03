from flask import Flask, render_template_string, request, redirect, url_for
import json
from pathlib import Path
from process_documents import extract_text_from_file, save_record

UPLOAD_FOLDER = Path('uploads')
UPLOAD_FOLDER.mkdir(exist_ok=True)

app = Flask(__name__)

data_file = Path('processed_data.json')

template = """
<!doctype html>
<html>
  <head>
    <title>Production Records</title>
  </head>
  <body>
    <h1>Processed Documents</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file" required>
      <button type="submit">Extract</button>
    </form>
    {% if records %}
      <ul>
        {% for r in records %}
          <li>
            <strong>{{ r.file_name }}</strong> - {{ r.timestamp }}<br>
            <pre>{{ r.extracted_text }}</pre>
          </li>
        {% endfor %}
      </ul>
    {% else %}
      <p>No records found.</p>
    {% endif %}
  </body>
</html>
"""


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        uploaded = request.files.get('file')
        if uploaded and uploaded.filename:
            file_path = UPLOAD_FOLDER / uploaded.filename
            uploaded.save(file_path)
            text = extract_text_from_file(file_path)
            save_record(uploaded.filename, text)
            return redirect(url_for('index'))

    records = []
    if data_file.exists():
        with open(data_file, 'r') as f:
            records = json.load(f)
    return render_template_string(template, records=records)


if __name__ == '__main__':
    app.run(debug=True)
