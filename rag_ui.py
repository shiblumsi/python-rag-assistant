import streamlit as st
import requests
import base64

# Page config
st.set_page_config(page_title="🧠 RAG Assistant", layout="wide")

# App Header
st.markdown("""
    <h1 style='text-align: center; color: #4B8BBE;'>🧠 RAG Assistant</h1>
    <p style='text-align: center; font-size: 18px;'>Upload documents or images, ask questions, and get AI-powered answers!</p>
    <hr style='margin-bottom: 30px;' />
""", unsafe_allow_html=True)

# API_URL for backend endpoint
API_URL = "https://shiblumsi-python-rag-api.hf.space"
#API_URL = "http://localhost:8000"

# Layout columns
col1, col2 = st.columns([1, 2], gap="large")

# === LEFT COLUMN: Upload file ===
with col1:
    st.markdown("### 📤 Upload Document")
    uploaded_file = st.file_uploader("Select a file", type=["pdf", "docx", "txt", "csv", "jpg", "jpeg", "png", "db"])

# === RIGHT COLUMN: Question + Optional Image ===
with col2:
    st.markdown("### ❓ Ask a Question")

    # Set default question state
    if "question" not in st.session_state:
        st.session_state.question = ""

    # Show question input box with session state value
    question = st.text_input("Type your question here...", value=st.session_state.question)

    # Smaller, compact Optional Image Input
    st.markdown("#### 📷 Optional Image Input", unsafe_allow_html=True)
    st.markdown("<p style='font-size:12px; font-style:italic; margin-top:-10px; margin-bottom:5px;'>You can also upload an image to assist your question.</p>", unsafe_allow_html=True)
    image_file = st.file_uploader(
        "Upload image (optional)",
        type=["jpg", "jpeg", "png"],
        key="img",
        help="Limit 20MB per file • JPG, JPEG, PNG",
        label_visibility="collapsed"
    )
    st.markdown("<div style='margin-bottom:15px;'></div>", unsafe_allow_html=True)

    ask_btn = st.button("🧠 Get Answer")

    if ask_btn:
        if not question.strip():
            st.warning("⚠️ Please enter a question.")
        else:
            st.session_state.question = question  # Save question to session state

            # Step 1: Upload file (if any)
            if uploaded_file:
                with st.spinner("📤 Uploading file and indexing..."):
                    files = {"file": (uploaded_file.name, uploaded_file, uploaded_file.type)}
                    upload_response = requests.post(f"{API_URL}/upload", files=files)
                    if upload_response.status_code == 200:
                        st.success("✅ File uploaded successfully.")
                    else:
                        st.error(f"❌ Upload failed: {upload_response.text}")
                        st.stop()

            # Step 2: Build query payload
            payload = {"question": question}

            if image_file:
                with st.spinner("📷 Encoding image..."):
                    image_bytes = image_file.read()
                    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
                    payload["image_base64"] = f"data:image/jpeg;base64,{encoded_image}"

            # Step 3: Query
            with st.spinner("🧠 Thinking..."):
                response = requests.post(f"{API_URL}/query", json=payload)

            if response.status_code == 200:
                result = response.json()

                st.markdown("### ✅ Answer")
                st.success(result["answer"])

                # 🧹 Clear the question input after getting the answer
                st.session_state.question = ""
            else:
                st.error(f"❌ Failed to get answer: {response.text}")
