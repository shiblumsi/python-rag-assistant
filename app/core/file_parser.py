import pdfplumber
import docx
import pytesseract
from PIL import Image
import pandas as pd
import sqlite3
import os

def extract_text_from_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text

def extract_text_from_docx(file_path):
    doc = docx.Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_from_txt(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_text_from_image(file_path):
    image = Image.open(file_path)
    return pytesseract.image_to_string(image)

def extract_text_from_csv(file_path):
    df = pd.read_csv(file_path)
    return df.to_string(index=False)

def extract_text_from_sqlite(file_path):
    conn = sqlite3.connect(file_path)
    cursor = conn.cursor()
    text = ""
    for table_name in get_table_names(cursor):
        rows = cursor.execute(f"SELECT * FROM {table_name}").fetchall()
        text += f"Table: {table_name}\n"
        for row in rows:
            text += str(row) + "\n"
    conn.close()
    return text

def get_table_names(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    return [row[0] for row in cursor.fetchall()]

def extract_text(file_path):
    ext = os.path.splitext(file_path)[1].lower()

    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext == '.docx':
        return extract_text_from_docx(file_path)
    elif ext == '.txt':
        return extract_text_from_txt(file_path)
    elif ext in ['.jpg', '.jpeg', '.png']:
        return extract_text_from_image(file_path)
    elif ext == '.csv':
        return extract_text_from_csv(file_path)
    elif ext == '.db':
        return extract_text_from_sqlite(file_path)
    else:
        return "Unsupported file format"
