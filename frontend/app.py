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