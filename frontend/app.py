import uuid
import requests
import streamlit as st

BACKEND_URL = "http:localhost:8000"

st.set_page_config(
    page_title="DEMO RAG APP",
    layout="wide",
)

def initialize_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "documents" not in st.session_state:
        st.session_state.documents = []
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())

def load_documents():
    try:
        response = requests.get(f"{BACKEND_URL}/documents")
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as error:
        st.error(f"Could not load documents: {error}")
        return []

    if isinstance(data, dict):
        return data.get("documents", [])
    if isinstance(data, list):
        return data
    return []

def upload_pdf(file):
    files = {"file": (file.name, file.getvalue(), "application/pdf")}
    response = requests.post(f"{BACKEND_URL}/upload", files=files)
    response.raise_for_status()
    return response.json()

def delete_document(document_id):
    response = requests.delete(f"{BACKEND_URL}/documents/{document_id}")
    response.raise_for_status()
    return response.json()

def ask_question(question):
    payload = {"question": question, "session_id": st.session_state.session_id}
    response = requests.post(f"{BACKEND_URL}/chat", json=payload)
    response.raise_for_status()
    return response.json()

def render_sidebar():
    with st.sidebar:
        st.title("Documents")

        uploaded_file = st.file_uploader("Choose a file", type=["pdf"])
        if uploaded_file is not None:
            if st.button("Upload", use_container_width=True):
                with st.spinner():
                    try:
                        upload_pdf(uploaded_file)
                        st.toast(f"Successfully uploaded {uploaded_file.name}")
                        st.session_state.documents = load_documents()
                        st.rerun()
                    except requests.RequestException as error:
                        st.error(f"Upload failed with error: {error}")
        st.divider()

        st.subheader("Indexed documents")

        if not st.session_state.documents:
            st.caption("No documents uploaded. Upload a pdf file to get started.")
        else:
            for doc in st.session_state.documents:
                col_name, col_delete = st.columns([4, 1])
                col_name.write(doc.get("filename", "Unnamed"))
                if col_delete.button("X", key=f"delete_{doc["document_id"]}", help="Delete document"):
                    try:
                        delete_document(doc["document_id"])
                        st.session_state.documents = load_documents()
                        st.rerun()
                    except requests.RequestException as error:
                        st.error(f"Delete failed with error: {error}")

        st.divider()

        if st.button("New chat", use_container_width=True):
            st.session_state.messages = []
            st.session_state.session_id = str(uuid.uuid4())
            st.rerun()