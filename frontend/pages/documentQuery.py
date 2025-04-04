import streamlit as st
import requests
import sys
import os

# Set page config
st.set_page_config(page_title="Document Query - RFP Bot", page_icon="🔍", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .query-container {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    .question {
        background: #e3f2fd;
        border-left: 5px solid #2196f3;
    }
    
    .answer {
        background: #f1f8e9;
        border-left: 5px solid #4caf50;
    }
    
    .section-header {
        color: #2E3192;
        font-size: 2em;
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .thread-info {
        background: #fff;
        padding: 1rem;
        border-radius: 8px;
        border-left: 5px solid #2E3192;
        margin-bottom: 1rem;
    }
    
    .stButton>button {
        background-color: #2E3192;
        color: white;
        border-radius: 5px;
        padding: 0.5rem 2rem;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #1BFFFF;
        color: #2E3192;
    }
    
    .stTextInput>div>div>input {
        border-radius: 5px;
        border: 2px solid #e0e0e0;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #2E3192;
        box-shadow: 0 0 0 2px rgba(46, 49, 146, 0.2);
    }

    .chat-history {
        background: white;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 2rem 0;
        max-height: 500px;
        overflow-y: auto;
    }

    .history-header {
        color: #2E3192;
        font-size: 1.5em;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #e0e0e0;
    }

    .timestamp {
        font-size: 0.8em;
        color: #666;
        margin-bottom: 0.5rem;
    }
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## WELCOME TO DOCUMENT QUERY")

# Flask server URL
BASE_URL = 'http://127.0.0.1:5500'
ASK_URL = f'{BASE_URL}/ask'
THREADS_URL = f'{BASE_URL}/threads'

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = {}

def get_threads():
    try:
        response = requests.get(THREADS_URL)
        if response.status_code == 200:
            return response.json().get('threads', [])
        else:
            st.error("Failed to fetch threads")
            return []
    except Exception as e:
        st.error(f"Error fetching threads: {str(e)}")
        return []

def create_thread(name):
    try:
        payload = {}
        if name.strip():
            payload['name'] = name.strip()
        response = requests.post(THREADS_URL, json=payload)
        if response.status_code == 201:
            data = response.json()
            thread_id = data.get('thread_id')
            thread_name = data.get('name')
            st.session_state.selected_thread = thread_id
            st.session_state.selected_thread_name = thread_name
            # Initialize chat history for new thread
            if thread_id not in st.session_state.chat_history:
                st.session_state.chat_history[thread_id] = []
            st.success(f"Thread '{thread_name}' created successfully! 🎉")
        else:
            st.error("Failed to create thread")
    except Exception as e:
        st.error(f"Error creating thread: {str(e)}")

def delete_thread(thread_id):
    try:
        response = requests.delete(f"{THREADS_URL}/{thread_id}")
        if response.status_code == 200:
            st.success(f"Thread deleted successfully! 🗑️")
            if st.session_state.selected_thread == thread_id:
                st.session_state.selected_thread = None
                st.session_state.selected_thread_name = None
            # Clear chat history for deleted thread
            if thread_id in st.session_state.chat_history:
                del st.session_state.chat_history[thread_id]
        else:
            st.error("Failed to delete thread")
    except Exception as e:
        st.error(f"Error deleting thread: {str(e)}")

def ask_question(question, thread_id):
    if not question:
        st.error("Please enter a question ❗")
        return

    with st.spinner('Processing your question... 🤔'):
        payload = {"question": question, "thread_id": thread_id}
        try:
            response = requests.post(ASK_URL, json=payload)
            response_data = response.json()

            if response.status_code == 200:
                # Add to chat history
                if thread_id not in st.session_state.chat_history:
                    st.session_state.chat_history[thread_id] = []
                
                st.session_state.chat_history[thread_id].append({
                    'question': question,
                    'answer': response_data.get("response", "No response received."),
                    'timestamp': st.session_state.get('current_time', 'Now')
                })

                # Display the latest Q&A
                st.markdown(f"""
                    <div class="chat-message question">
                        <strong>Question:</strong><br>{question}
                    </div>
                    <div class="chat-message answer">
                        <strong>Answer:</strong><br>{response_data.get("response", "No response received.")}
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.error("Error: " + response_data.get("error", "An error occurred."))
        except Exception as e:
            st.error(f"Request failed: {str(e)}")

# Initialize session state
if 'selected_thread' not in st.session_state:
    st.session_state.selected_thread = None
if 'selected_thread_name' not in st.session_state:
    st.session_state.selected_thread_name = None

# Main content area
st.markdown('<h1 class="section-header">Document Query 📚</h1>', unsafe_allow_html=True)

# Sidebar for thread management
with st.sidebar:
    st.markdown("### Thread Management 🧵")
    thread_name_input = st.text_input("New Thread Name (optional)", placeholder="Enter thread name...")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Create Thread ➕"):
            create_thread(thread_name_input)
            threads = get_threads()
    
    threads = get_threads()
    
    if threads:
        st.markdown("### Select Thread 📑")
        thread_options = {thread['name']: thread['id'] for thread in threads}
        selected_thread_name = st.selectbox(
            "Choose a conversation thread",
            list(thread_options.keys()),
            key="thread_select"
        )
        selected_thread_id = thread_options[selected_thread_name]
        st.session_state.selected_thread = selected_thread_id
        st.session_state.selected_thread_name = selected_thread_name
        
        with col2:
            if st.button("Delete Thread 🗑️"):
                delete_thread(selected_thread_id)
                threads = get_threads()
                st.rerun()
    else:
        st.info("No threads available. Create one to get started! 🚀")

# Main query area
if st.session_state.selected_thread:
    st.markdown(f"""
        <div class="thread-info">
            <h3>Active Thread: {st.session_state.selected_thread_name} 🔵</h3>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="query-container">', unsafe_allow_html=True)
        st.markdown("### Ask Your Question 💭")
        question = st.text_input("", placeholder="Type your question here...", key="question_input")
        if st.button("Send Question 📤"):
            ask_question(question, st.session_state.selected_thread)
        st.markdown('</div>', unsafe_allow_html=True)

        # Display chat history
        if st.session_state.selected_thread in st.session_state.chat_history and st.session_state.chat_history[st.session_state.selected_thread]:
            st.markdown('<div class="chat-history">', unsafe_allow_html=True)
            st.markdown('<div class="history-header">Conversation History 💬</div>', unsafe_allow_html=True)
            
            for message in reversed(st.session_state.chat_history[st.session_state.selected_thread]):
                st.markdown(f"""
                    <div class="timestamp">⏰ {message['timestamp']}</div>
                    <div class="chat-message question">
                        <strong>Question:</strong><br>{message['question']}
                    </div>
                    <div class="chat-message answer">
                        <strong>Answer:</strong><br>{message['answer']}
                    </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("👈 Please select or create a thread in the sidebar to start querying documents.")
    