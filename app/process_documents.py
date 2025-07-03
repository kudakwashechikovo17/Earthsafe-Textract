import argparse
import json
import boto3
from datetime import datetime
from pathlib import Path


def extract_text_from_file(file_path):
    client = boto3.client('textract')
    with open(file_path, 'rb') as document:
        image_bytes = document.read()

    response = client.detect_document_text(Document={'Bytes': image_bytes})
    lines = [item['Text'] for item in response.get('Blocks', []) if item['BlockType'] == 'LINE']
    return '\n'.join(lines)


def save_record(file_name, extracted_text, output_file='processed_data.json'):
    record = {
        'file_name': file_name,
        'extracted_text': extracted_text,
        'timestamp': datetime.utcnow().isoformat()
    }
    data = []
    path = Path(output_file)
    if path.exists():
        with open(path, 'r') as f:
            data = json.load(f)
    data.append(record)
    with open(path, 'w') as f:
        json.dump(data, f, indent=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process scanned documents using Amazon Textract.')
    parser.add_argument('file', help='Path to the scanned image file')
    args = parser.parse_args()

    text = extract_text_from_file(args.file)
    save_record(args.file, text)
    print(f"Processed {args.file}")
