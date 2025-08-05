# 🧠 Python RAG Assistant

A smart Retrieval-Augmented Generation (RAG) API built with FastAPI and Streamlit.  
Supports querying text and images using OCR, document chunking, FAISS vector search, and LLM-based answers.

---

## 🚀 Features

- Upload files (PDF, DOCX, TXT, CSV, JPG, JPEG, PNG)  
- Ask questions about uploaded documents or images  
- OCR support for images  
- Vector similarity search with FAISS  
- Simple Streamlit frontend UI for upload + query  

---

## ⚙️ Environment Setup

### Requirements:
- Python 3.10+
- pip
- virtualenv (recommended)

## 📋 Instructions
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/python-rag-assistant.git
   cd python-rag-assistant
   ```

2. Create & activate a virtual environment:
```
python -m venv venv
```
- On Linux/macOS:
```
source venv/bin/activate
```
- On Windows:
```
venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

5. Create a .env file with your OpenRouter API key:
```
OPENROUTER_API_KEY=openrouter_api_key_here
```

7. Run the backend API server:
```
uvicorn app.main:app --reload
```

9. Run the Streamlit frontend:
```
streamlit run streamlit_ui.py
```

---

## 🔌 API Usage

### 1. `/upload` (POST)
- **Description:** Uploads and indexes a file.
- **Supported Files:** PDF, DOCX, TXT, CSV, JPG, PNG
- **Request:** `multipart/form-data`
- **Response:**
```json
{
  "message": "Uploaded and indexed",
  "total_chunks": 21,
  "source_file": "document.pdf"
}
```
### 2. `/query` (POST)
- Description: Sends a question to the RAG system. Optionally supports image input.

Request (JSON):

```json

{
  "question": "What is the summary?",
  "image_base64": "data:image/jpeg;base64,..."
}
```
Response:

```json

{
  "question": "What is the summary?",
  "answer": "The document describes...",
  "context_snippet": "Text from file...",
  "sources": [
    {
      "file": "xyz.pdf",
      "chunk": 3
    }
  ]
}
```

