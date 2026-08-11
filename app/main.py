from collections import defaultdict
import os
import sys
from components.file_uploader import file_uploader
from components.chat_history_upload_files import conversation_history_uploaded_files
from utility.temp_file_helper import get_uploaded_path
from utility.utils import load_css
from components.chatbot import assistant_reply, user_query, display_chat_messages
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from loader.loader import load_file
from vector_store.vector_store import create_and_save_vector_db
from embeddings.embed import embed_vector
import streamlit as st
from PIL import Image
logo = Image.open("assets/logo.png")

st.set_page_config(
    page_icon=logo,
    page_title='VectorDocs'
)
load_css()

if "chat_sessions" not in st.session_state:
    st.session_state.chat_sessions = {}

if "metadata_file" not in st.session_state:
    st.session_state.metadata_file = defaultdict(str)
if "current_session" not in st.session_state:
    st.session_state.current_session = "New Chat"
    st.session_state.chat_sessions[st.session_state.current_session] = {
        "messages": [],
        "files": set(),
        "current_file":"",
        "faiss_upload":False
    }
if "uploaded_file_url" not in st.session_state:
    st.session_state.uploaded_file_url = defaultdict(dict)

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state.OPENAI_API_KEY = None

col1,col2 = st.columns([1,4], gap="small")
with col1:
    
    st.image(logo, width=125) 
with col2:
    st.title("VectorDocs 🧠🤖")

content_file = file_uploader()


tmp_path = get_uploaded_path(content_file)
if content_file:
    conversation_history_uploaded_files(content_file.name,tmp_path)
    
else:
    conversation_history_uploaded_files(None,tmp_path)



current_file = st.session_state.chat_sessions[st.session_state.current_session].get("current_file", "") if st.session_state.chat_sessions else ""
if current_file:
    st.info(f"📂 Currently uploaded file for this session: **{current_file}**")
    st.session_state.chat_sessions[st.session_state.current_session]["faiss_upload"] = False
else:
    st.warning("⚠️ No file uploaded yet for this session.")


display_chat_messages()

print(st.session_state.chat_sessions[st.session_state.current_session]["faiss_upload"])

if content_file is not None and not st.session_state.chat_sessions[st.session_state.current_session]["faiss_upload"]:
    with st.spinner('Uploading into FAISS ..'):
        content = load_file(tmp_path)
        create_and_save_vector_db(content)
        st.session_state.chat_sessions[st.session_state.current_session]["faiss_upload"] = True


query = st.chat_input('Hello from VectorDocs!')
if content_file is not None:
    if query and st.session_state.OPENAI_API_KEY:
        user_query(query)
        with st.spinner('Loading ..'):
            ai_response = embed_vector(query)
            assistant_reply(ai_response)
        st.rerun()
if query and content_file is None:
    st.info('Please upload file while querying')
