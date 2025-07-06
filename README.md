# Earthsafe Textract Prototype

This repository contains a small prototype for digitizing gold production records. It shows how to use **Amazon Textract** to process scanned receipts and view the extracted information from a simple dashboard.

## Setup
nhj
1. Install the requirements (preferably in a virtual environment):

   ```bash
   pip install -r app/requirements.txt
   ```

2. Configure AWS credentials so that `boto3` can access Amazon Textract.

## Processing a Document

Run `process_documents.py` with the path to a scanned image file:

```bash
python app/process_documents.py /path/to/receipt.jpg
```

The script saves extracted data to `processed_data.json`.

## Viewing the Dashboard

Start the Flask application:

```bash
python app/app.py
```

Open `http://localhost:5000` in a browser to see the records.

This is a basic example intended for experimentation. It can be extended to store data in a real database and include user authentication for a production deployment.
