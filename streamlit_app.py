
import uuid

import requests
import streamlit as st

API_BASE_URL = "http://127.0.0.1:8000/api/v1"


def call_upload_api(file) -> dict:
    """Send a file to the backend's /upload endpoint."""
    files = {"file": (file.name, file.getvalue(), file.type)}
    response = requests.post(f"{API_BASE_URL}/upload", files=files)
    response.raise_for_status()
    return response.json()


def call_chat_api(session_id: str, message: str) -> dict:
    """Send a chat message to the backend's /chat endpoint."""
    payload = {"session_id": session_id, "message": message}
    response = requests.post(f"{API_BASE_URL}/chat", json=payload)
    response.raise_for_status()
    return response.json()


def init_session_state() -> None:
    if "session_id" not in st.session_state:
        st.session_state.session_id = str(uuid.uuid4())[:8]
    if "messages" not in st.session_state:
        st.session_state.messages = []


def render_sidebar() -> None:
    with st.sidebar:
        st.header("Document Upload")
        uploaded_file = st.file_uploader("Upload a PDF, TXT, or Markdown file", type=["pdf", "txt", "md"])

        if uploaded_file is not None and st.button("Upload & Index"):
            with st.spinner("Uploading and indexing..."):
                try:
                    result = call_upload_api(uploaded_file)
                    st.success(f"{result['message']} ({result['chunks_indexed']} chunks)")
                except requests.exceptions.HTTPError as exc:
                    detail = exc.response.json().get("detail", str(exc))
                    st.error(f"Upload failed: {detail}")
                except requests.exceptions.ConnectionError:
                    st.error("Could not reach the backend. Is it running on port 8000?")

        st.divider()
        st.caption(f"Session ID: `{st.session_state.session_id}`")
        if st.button("Start New Session"):
            st.session_state.session_id = str(uuid.uuid4())[:8]
            st.session_state.messages = []
            st.rerun()


def render_chat() -> None:
    st.title("Mini AI Assistant")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Ask a question...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = call_chat_api(st.session_state.session_id, user_input)
                    reply = result["reply"]
                except requests.exceptions.HTTPError as exc:
                    reply = f"Error: {exc.response.json().get('detail', str(exc))}"
                except requests.exceptions.ConnectionError:
                    reply = "Could not reach the backend. Is it running on port 8000?"
            st.write(reply)

        st.session_state.messages.append({"role": "assistant", "content": reply})


init_session_state()
render_sidebar()
render_chat()