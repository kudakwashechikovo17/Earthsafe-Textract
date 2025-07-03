from flask import Flask, render_template_string
import json
from pathlib import Path

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


@app.route('/')
def index():
    records = []
    if data_file.exists():
        with open(data_file, 'r') as f:
            records = json.load(f)
    return render_template_string(template, records=records)


if __name__ == '__main__':
    app.run(debug=True)
