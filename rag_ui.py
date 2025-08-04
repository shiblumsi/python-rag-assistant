import streamlit as st
import requests
import base64

st.set_page_config(page_title="RAG Assistant", layout="wide")
st.title("🧠 Retrieval-Augmented Generation (RAG) Assistant")

API_URL = "http://localhost:8000"

col1, col2 = st.columns([1, 2])  # Left: Upload, Right: Question

# === LEFT COLUMN: Upload file ===
with col1:
    st.header("📤 Upload File ")
    uploaded_file = st.file_uploader("Choose a document file", type=["pdf", "docx", "txt", "csv", "jpg", "jpeg", "png", "db"])

# === RIGHT COLUMN: Question + Optional Image ===
with col2:
    st.header("❓ Ask a Question",divider="gray")
    question = st.text_input("Enter your question")

    st.subheader("📷 Optional: Upload Image (jpg/jpeg/png)")
    image_file = st.file_uploader("Choose an image (optional)", type=["jpg", "jpeg", "png"])

    if st.button("🧠 Get Answer"):
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            # Step 1: If file is uploaded, send to /upload API
            if uploaded_file:
                with st.spinner("📤 Uploading file and indexing..."):
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    upload_response = requests.post(f"{API_URL}/upload", files=files)
                    if upload_response.status_code == 200:
                        st.success("✅ File uploaded successfully.")
                    else:
                        st.error(f"❌ Upload failed: {upload_response.text}")
                        st.stop()

            # Step 2: Prepare query payload
            payload = {"question": question}

            if image_file:
                with st.spinner("📷 Encoding image..."):
                    image_bytes = image_file.read()
                    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                    payload["image_base64"] = f"data:image/jpeg;base64,{encoded_image}"

            # Step 3: Send to /query
            with st.spinner("🧠 Generating answer..."):
                response = requests.post(f"{API_URL}/query", json=payload)

            if response.status_code == 200:
                result = response.json()

                st.markdown("### ✅ Answer")
                st.success(result["answer"])

                st.markdown("### 📚 Context Snippet")
                st.code(result.get("context_snippet", "N/A"))

                st.markdown("### 📎 Source Info")
                if "sources" in result:
                    for src in result["sources"]:
                        st.write(f"📄 File: `{src['file']}`, 🔢 Chunk: {src['chunk']}")
            else:
                st.error(f"❌ Error: {response.status_code} - {response.text}")
