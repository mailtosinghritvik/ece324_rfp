import streamlit as st
import requests
import sys
import os
import base64
import socket
import time
import json

# Import the same styling as home page
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# Custom CSS for professional styling with improved readability - same as in home.py
st.markdown("""
    <style>
    /* Professional color palette with better contrast */
    :root {
        --primary: #2c5282;         /* Deep blue - professional */
        --primary-dark: #1a365d;    /* Darker blue for hover states */
        --secondary: #718096;       /* Medium slate gray for accents */
        --background: #f7fafc;      /* Light gray background */
        --card-bg: #ffffff;         /* Pure white card backgrounds */
        --text-primary: #1a202c;    /* Very dark gray for primary text */
        --text-secondary: #2d3748;  /* Dark gray for secondary text */
        --text-light: #4a5568;      /* Medium gray for tertiary text */
        --border: #e2e8f0;          /* Light gray borders */
        --success: #2f855a;         /* Green for success messages */
        --info: #3182ce;            /* Blue for info messages */
        --warning: #dd6b20;         /* Orange for warnings */
        --error: #e53e3e;           /* Red for errors */
        --shadow: rgba(0,0,0,0.1);  /* Shadow with better visibility */
    }
    
    /* Base styles */
    .stApp {
        background-color: var(--background);
        background-image: none;
        color: var(--text-primary);
    }
    
    /* Typography - improved readability */
    body {
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
        color: var(--text-primary);
        line-height: 1.6;
        font-size: 16px;
    }
    
    h1 {
        color: var(--text-primary);
        font-weight: 700;
        margin-bottom: 1rem;
        font-size: 2.2rem;
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }
    
    h2 {
        color: var(--text-primary);
        font-weight: 600;
        margin-top: 1.8rem;
        margin-bottom: 1.2rem;
        font-size: 1.6rem;
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }
    
    h3 {
        color: var(--text-primary);
        font-weight: 600;
        margin-top: 1.6rem;
        margin-bottom: 0.8rem;
        font-size: 1.3rem;
        font-family: 'Inter', 'Helvetica Neue', Arial, sans-serif;
    }
    
    p, li {
        color: var(--text-secondary);
        font-size: 1rem;
        margin-bottom: 1rem;
        line-height: 1.6;
    }
    
    /* Header styling - cleaner and more professional */
    .main-header {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        margin-bottom: 2rem;
        border-left: 4px solid var(--primary);
        position: relative;
    }
    
    /* Card styling with better visibility */
    .content-section {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        margin-bottom: 2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    /* Chat styling with improved readability */
    .chat-container {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px var(--shadow);
        position: relative;
    }
    
    .chat-message {
        padding: 1.25rem;
        margin-bottom: 1.25rem;
        border-radius: 8px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
        position: relative;
        line-height: 1.6;
        font-size: 1rem;
    }
    
    .user-message {
        background: rgba(44,82,130,0.08);
        margin-left: 2.5rem;
        margin-right: 1.25rem;
        border-top-left-radius: 4px;
        color: var(--text-primary);
    }
    
    .user-message::before {
        content: "";
        position: absolute;
        left: -40px;
        top: 50%;
        transform: translateY(-50%);
        width: 32px;
        height: 32px;
        background-color: #cbd5e0;
        background-image: url('https://cdn-icons-png.flaticon.com/512/149/149071.png');
        background-size: cover;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    .assistant-message {
        background: rgba(49,130,206,0.08);
        margin-right: 2.5rem;
        margin-left: 1.25rem;
        border-top-right-radius: 4px;
        color: var(--text-primary);
    }
    
    .assistant-message::before {
        content: "";
        position: absolute;
        right: -40px;
        top: 50%;
        transform: translateY(-50%);
        width: 32px;
        height: 32px;
        background-color: #bee3f8;
        background-image: url('https://cdn-icons-png.flaticon.com/512/4712/4712027.png');
        background-size: cover;
        border-radius: 50%;
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
    }
    
    /* Button styling - cleaner with better contrast */
    .stButton > button {
        background: var(--primary);
        color: white;
        border: none;
        font-weight: 600;
        padding: 0.7rem 1.25rem;
        border-radius: 6px;
        transition: all 0.2s ease;
        font-size: 1rem;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }
    
    .stButton > button:hover {
        background: var(--primary-dark);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
    }
    
    /* Input styling with better focus states */
    .stTextInput > div > div {
        background: white;
        border-radius: 6px;
        border: 1px solid var(--border);
        transition: all 0.2s ease;
        font-size: 1rem;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div:focus-within {
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(49,130,206,0.2);
    }
    
    /* Input text color fix */
    .stTextInput > div > div > input {
        color: var(--text-primary) !important;
        font-size: 1rem;
    }
    
    .stTextArea > div > div > textarea {
        color: var(--text-primary) !important;
        font-size: 1rem;
    }
    
    .stSelectbox > div > div > div > div {
        color: var(--text-primary) !important;
        font-size: 1rem;
    }
    
    /* Navbar styling - more professional */
    .navbar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem 2rem;
        background-color: var(--card-bg);
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        position: fixed;
        top: 0;
        right: 0;
        left: 0;
        z-index: 1000;
    }

    .navbar-logo {
        display: flex;
        align-items: center;
    }

    .navbar-logo-text {
        font-weight: 700;
        font-size: 1.2rem;
        color: var(--primary);
    }

    .navbar-links {
        display: flex;
        gap: 1.5rem;
    }

    .navbar-link {
        font-weight: 500;
        color: var(--text-light);
        cursor: pointer;
        padding: 0.5rem;
        border-radius: 4px;
        transition: all 0.2s ease;
    }

    .navbar-link:hover {
        color: var(--primary);
        background-color: rgba(49,130,206,0.08);
    }

    .navbar-link.active {
        color: var(--primary);
        font-weight: 600;
    }

    .nav-button {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 6px;
        padding: 0.7rem 1.25rem;
        font-weight: 600;
        margin-left: 1rem;
        cursor: pointer;
        font-size: 1rem;
        text-decoration: none;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
    }

    .nav-button:hover {
        background-color: var(--primary-dark);
    }

    .main-content {
        margin-top: 5rem;
        padding: 2rem;
    }

    /* Message styles */
    .message {
        margin-bottom: 1.25rem;
        padding: 1rem;
        border-radius: 8px;
        max-width: 80%;
    }

    .user-message {
        background-color: #ebf8ff;
        margin-left: auto;
        color: var(--text-primary);
    }

    .assistant-message {
        background-color: #f0fff4;
        margin-right: auto;
        color: var(--text-primary);
    }

    .message-text {
        margin: 0;
        line-height: 1.5;
    }

    /* Input container */
    .input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 1.5rem;
        background-color: white;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
    }

    .input-box {
        width: 100%;
        padding: 0.75rem;
        border: 1px solid var(--border);
        border-radius: 6px;
        margin-bottom: 0.75rem;
    }
    </style>
""", unsafe_allow_html=True)

# Top navbar instead of sidebar
st.markdown(f"""
<div class="navbar">
    <div class="navbar-logo">
        <span class="navbar-logo-text">Document AI Assistant</span>
    </div>
    <div class="navbar-links">
        <span class="navbar-link" id="home-link">Home</span>
        <span class="navbar-link active" id="chat-link">Chat</span>
        <span class="navbar-link" id="upload-link">Upload</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Use Streamlit buttons for navigation instead of JavaScript
col1, col2, col3 = st.columns([1,1,1])
with col1:
    st.write("""
    <a href="/" target="_self">
        <button style="
            background-color: #5b6bb8;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.25rem;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            font-size: 1.05rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        ">
            🏠 Home
        </button>
    </a>
    """, unsafe_allow_html=True)
with col2:
    pass  # Already on Chat page
with col3:
    st.write("""
    <a href="/fileUploader" target="_self">
        <button style="
            background-color: #5b6bb8;
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.7rem 1.25rem;
            font-weight: 600;
            width: 100%;
            cursor: pointer;
            font-size: 1.05rem;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        ">
            📤 Upload
        </button>
    </a>
    """, unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('''
<div style="position: relative; z-index: 2; display: flex; align-items: center;">
    <div style="flex: 3;">
        <h1>Document Q&A</h1>
        <p>Ask questions about your uploaded documents and get precise answers</p>
    </div>
    <div style="flex: 1; text-align: right;">
        <img src="https://cdn-icons-png.flaticon.com/512/4253/4253264.png" style="max-width: 100px; border-radius: 8px;">
    </div>
</div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Backend URL configuration
BACKEND_URL = "http://127.0.0.1:5500"
THREADS_URL = f"{BACKEND_URL}/threads"
ASK_URL = f"{BACKEND_URL}/ask"
UPLOAD_URL = f"{BACKEND_URL}/upload"

# Functions
def get_threads():
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.get(THREADS_URL, timeout=10)
            if response.status_code == 200:
                return response.json()
            else:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                st.error(f"Error fetching threads: {response.text}")
                return []
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            st.error("Cannot connect to the backend server. Please ensure the Flask server is running.")
            return []

def create_thread():
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.post(THREADS_URL, timeout=10)
            if response.status_code == 201:
                return response.json()["thread_id"]
            else:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                st.error(f"Error creating thread: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            st.error("Cannot connect to the backend server. Please ensure the Flask server is running.")
            return None

def ask_question(thread_id, question):
    max_retries = 3
    retry_delay = 1  # seconds
    
    for attempt in range(max_retries):
        try:
            response = requests.post(ASK_URL, json={"thread_id": thread_id, "question": question}, timeout=10)
            if response.status_code == 200:
                return response.json()["response"]
            else:
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                    continue
                st.error(f"Error asking question: {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
                continue
            st.error("Cannot connect to the backend server. Please ensure the Flask server is running.")
            return None

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "thread_id" not in st.session_state:
    st.session_state.thread_id = None

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Thread management section with improved layout
st.markdown("""
<div class="content-section">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem;">
        <div>
            <h2 style="margin-top: 0; margin-bottom: 0.5rem;">Thread Management</h2>
            <p style="margin-bottom: 0;">Create a new thread or select an existing one to start chatting.</p>
        </div>
        <div style="text-align: right;">
            <img src="https://cdn-icons-png.flaticon.com/512/2797/2797387.png" style="width: 48px; height: 48px; opacity: 0.8;">
        </div>
    </div>
    
    <div style="background-color: rgba(44,82,130,0.03); padding: 1.5rem; border-radius: 6px; margin-top: 1.5rem;">
        <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--primary);">Create New Thread</h3>
""", unsafe_allow_html=True)

# Create new thread with improved layout
col1, col2 = st.columns([3, 1])
with col1:
    thread_name = st.text_input("Thread Name (optional)", key="thread_name_input", 
                               placeholder="Enter a name for your new thread")
with col2:
    if st.button("Create Thread", key="create_thread_button"):
        with st.spinner("Creating thread..."):
            thread_id = create_thread()
            if thread_id:
                st.session_state.thread_id = thread_id
                st.session_state.messages = []
                st.success("Thread created successfully!")
                time.sleep(1)  # Give user time to see the success message
                st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)

# Display existing threads with improved UI
st.markdown("""
<div style="margin-top: 1.5rem;">
    <h3 style="font-size: 1.2rem; color: var(--primary);">Existing Threads</h3>
</div>
""", unsafe_allow_html=True)

threads = get_threads()
if threads:
    # Sort threads by most recent first (assuming thread ID is time-based)
    threads.sort(key=lambda x: x['id'], reverse=True)
    
    selected_thread = st.selectbox(
        "Select a Thread",
        options=[thread["name"] or f"Thread {thread['id']}" for thread in threads],
        index=None if not st.session_state.thread_id else next(
            (i for i, thread in enumerate(threads) 
             if thread["id"] == st.session_state.thread_id), 
            None
        )
    )
    
    if selected_thread:
        thread_id = next(
            (thread["id"] for thread in threads 
             if (thread["name"] or f"Thread {thread['id']}") == selected_thread),
            None
        )
        if thread_id and thread_id != st.session_state.thread_id:
            st.session_state.thread_id = thread_id
            st.session_state.messages = []
            st.experimental_rerun()
else:
    st.markdown("""
    <div style="padding: 1.5rem; text-align: center; background-color: rgba(44,82,130,0.03); border-radius: 6px; border-left: 3px solid var(--info);">
        <img src="https://cdn-icons-png.flaticon.com/512/6134/6134065.png" style="width: 60px; margin-bottom: 1rem; opacity: 0.7;">
        <p style="margin-bottom: 0;">No existing threads found. Create a new one to start chatting!</p>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Add document upload section
st.markdown("""
<div class="content-section" style="margin-top: 2rem;">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem;">
        <div>
            <h2 style="margin-top: 0; margin-bottom: 0.5rem;">Upload Documents</h2>
            <p style="margin-bottom: 0;">Add documents to enhance your conversation with AI.</p>
        </div>
        <div style="text-align: right;">
            <img src="https://cdn-icons-png.flaticon.com/512/4319/4319077.png" style="width: 48px; height: 48px; opacity: 0.8;">
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Upload PDF Document", type=['pdf'])

if uploaded_file is not None:
    st.markdown("""
    <div style="background-color: rgba(44,82,130,0.03); padding: 1.5rem; border-radius: 8px; margin-top: 1rem; border-left: 3px solid var(--primary);">
        <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--primary);">Selected File</h3>
    """, unsafe_allow_html=True)
    
    st.write(f"Filename: {uploaded_file.name}")
    st.write(f"Size: {uploaded_file.size/1024:.2f} KB")
    
    if st.button("Process Document", key="process_document_button"):
        with st.spinner("Uploading and processing document..."):
            try:
                files = {"file": uploaded_file}
                response = requests.post(UPLOAD_URL, files=files)
                
                if response.status_code == 200:
                    st.success("Document uploaded and processed successfully!")
                else:
                    st.error(f"Error uploading document: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div style="text-align: center; padding: 2rem 1.5rem; background-color: rgba(44,82,130,0.02); border-radius: 8px; cursor: pointer;" onclick="document.querySelector('.css-1cpxqw2').click()">
        <img src="https://cdn-icons-png.flaticon.com/512/2965/2965335.png" style="width: 64px; margin-bottom: 1rem; opacity: 0.7;">
        <p>Click to upload a PDF document or drag and drop</p>
        <p style="font-size: 0.9rem; margin-top: 0.5rem; color: var(--text-light);">Supported format: PDF</p>
    </div>
    """, unsafe_allow_html=True)

# Chat interface with improved UI
if st.session_state.thread_id:
    st.markdown("""
    <div class="content-section" style="margin-top: 2rem;">
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1.2rem;">
            <div>
                <h2 style="margin-top: 0; margin-bottom: 0.5rem;">Document Chat</h2>
                <p style="margin-bottom: 0;">Ask questions about your documents and get AI-powered responses.</p>
            </div>
            <div style="text-align: right;">
                <img src="https://cdn-icons-png.flaticon.com/512/2593/2593691.png" style="width: 48px; height: 48px; opacity: 0.8;">
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages with improved styling
    if st.session_state.messages:
        st.markdown('<div class="chat-container" style="background-color: rgba(44,82,130,0.02); padding: 1.5rem; border-radius: 8px; max-height: 500px; overflow-y: auto;">', unsafe_allow_html=True)
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.markdown(f"""
                <div class="chat-message user-message" style="display: flex; align-items: flex-start;">
                    <div style="flex-shrink: 0; width: 32px; height: 32px; border-radius: 50%; background-color: var(--primary); margin-right: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 14px;">U</div>
                    <div style="flex-grow: 1;">
                        <p class="message-text" style="margin: 0;">{message["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div class="chat-message assistant-message" style="display: flex; align-items: flex-start; margin-top: 1rem; margin-bottom: 1rem;">
                    <div style="flex-shrink: 0; width: 32px; height: 32px; border-radius: 50%; background-color: var(--info); margin-right: 12px; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 14px;">AI</div>
                    <div style="flex-grow: 1;">
                        <p class="message-text" style="margin: 0;">{message["content"]}</p>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1.5rem; background-color: rgba(44,82,130,0.02); border-radius: 8px;">
            <img src="https://cdn-icons-png.flaticon.com/512/3572/3572055.png" style="width: 80px; margin-bottom: 1.5rem; opacity: 0.7;">
            <h3 style="margin-bottom: 0.5rem; font-size: 1.3rem;">No messages yet</h3>
            <p style="color: var(--text-light);">Ask a question to start the conversation</p>
        </div>
        """, unsafe_allow_html=True)

    # Question input with improved UI
    st.markdown("""
    <div style="margin-top: 1.5rem; background-color: white; padding: 1.5rem; border-radius: 8px; border: 1px solid var(--border);">
        <h3 style="margin-top: 0; font-size: 1.2rem; color: var(--primary); margin-bottom: 1rem;">Ask a Question</h3>
    """, unsafe_allow_html=True)
    
    with st.container():
        question = st.text_area("Question", key="question_input", 
                              placeholder="Type your question about your documents here...",
                              height=100)
        
        col1, col2 = st.columns([5, 1])
        with col2:
            send_button = st.button("Send", key="send_button", use_container_width=True)
        
        if send_button:
            if question:
                with st.spinner("Getting response..."):
                    # Add user message
                    st.session_state.messages.append({"role": "user", "content": question})
                    
                    # Get AI response
                    response = ask_question(st.session_state.thread_id, question)
                    if response:
                        st.session_state.messages.append({"role": "assistant", "content": response})
                        st.experimental_rerun()
            else:
                st.warning("Please enter a question")
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    # Empty state with visual cue when no thread is selected
    st.markdown("""
    <div class="content-section" style="text-align: center; padding: 3rem 2rem; margin-top: 2rem;">
        <img src="https://cdn-icons-png.flaticon.com/512/8364/8364509.png" style="width: 100px; margin-bottom: 1.5rem; opacity: 0.7;">
        <h2 style="margin-bottom: 1rem;">Start Chatting with Your Documents</h2>
        <p style="margin-bottom: 2rem; max-width: 600px; margin-left: auto; margin-right: auto;">Please create a new thread or select an existing thread to begin asking questions about your documents.</p>
        <div style="background-color: rgba(44,82,130,0.05); padding: 1rem; border-radius: 6px; display: inline-block;">
            <p style="margin-bottom: 0;">👆 Use the thread management section above to get started</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)
    
