import streamlit as st
import requests

st.set_page_config(page_title="RAG Assistant", layout="wide")

st.title("📄 Retrieval-Augmented Generation (RAG) Assistant")
st.markdown("Upload your files and ask questions based on their content.")

API_URL = "http://localhost:8000"

# Two-column layout
col1, col2 = st.columns([1, 2])  # 1:2 ratio

# 📤 File Upload in Left Column
with col1:
    st.header("📤 Upload File")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "txt", "csv"])

    if uploaded_file:
        with st.spinner("Uploading and indexing..."):
            files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
            response = requests.post(f"{API_URL}/upload", files=files)

        if response.status_code == 200:
            st.success("✅ File uploaded and processed successfully.")
        else:
            st.error(f"❌ Upload failed: {response.text}")

# ❓ Question & Answer in Right Column
with col2:
    st.header("❓ Ask a Question")
    question = st.text_input("Enter your question")

    if st.button("🧠 Get Answer"):
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            with st.spinner("Generating answer..."):
                payload = {"question": question}
                response = requests.post(f"{API_URL}/query", json=payload)

            if response.status_code == 200:
                result = response.json()

                st.markdown("### ✅ Answer")
                st.success(result["answer"])

            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
