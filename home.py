import streamlit as st
import os
import base64

# Get the directory containing the current script
current_dir = os.path.dirname(os.path.abspath(__file__))

# Set page configuration
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for professional styling with improved readability
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
    
    .subtitle {
        color: var(--text-secondary);
        font-size: 1.3rem;
        margin-bottom: 0;
        font-weight: 400;
        line-height: 1.5;
    }
    
    /* Card styling with better visibility */
    .content-section {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        margin-bottom: 2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
        border-top: 3px solid transparent;
    }
    
    .content-section:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 24px var(--shadow);
    }
    
    /* Card container with clean background */
    .card-container {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 2rem;
        margin-top: 2rem;
        position: relative;
    }
    
    /* Feature cards with modern design */
    .card {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        transition: all 0.3s ease;
        position: relative;
        border-top: 3px solid var(--primary);
        z-index: 1;
    }
    
    .card-content {
        position: relative;
        z-index: 1;
    }
    
    .card h3 {
        font-size: 1.4rem;
        margin-top: 1rem;
        margin-bottom: 1rem;
    }
    
    /* Button styling - cleaner with better contrast */
    .custom-button {
        background: var(--primary);
        color: white;
        font-weight: 600;
        padding: 0.85rem 1.5rem;
        border-radius: 6px;
        border: none;
        cursor: pointer;
        transition: background 0.2s ease, transform 0.1s ease;
        display: inline-block;
        text-decoration: none;
        text-align: center;
        box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        font-size: 1rem;
    }
    
    .custom-button:hover {
        background: var(--primary-dark);
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    }
    
    /* Icon styling - professional colors */
    .icon {
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
        width: 64px;
        height: 64px;
        border-radius: 8px;
        margin-bottom: 1rem;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .card:nth-child(1) .icon::before {
        background: linear-gradient(135deg, #2c5282 0%, #4299e1 100%);
    }
    
    .card:nth-child(2) .icon::before {
        background: linear-gradient(135deg, #2c5282 0%, #4299e1 100%);
    }
    
    .card:nth-child(3) .icon::before {
        background: linear-gradient(135deg, #2c5282 0%, #4299e1 100%);
    }
    
    /* Information boxes - better contrast */
    .info-box {
        padding: 1.5rem 1.5rem 1.5rem 4rem;
        border-radius: 8px;
        margin: 1.25rem 0;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    
    .info-box.tip {
        background-color: rgba(49,130,206,0.08);
        border-left: 4px solid var(--info);
    }
    
    .info-box.success {
        background-color: rgba(47,133,90,0.08);
        border-left: 4px solid var(--success);
    }
    
    .info-box::before {
        position: absolute;
        left: 1.25rem;
        top: 50%;
        transform: translateY(-50%);
        font-size: 1.75rem;
    }
    
    .info-box.tip::before {
        content: "💡";
    }
    
    .info-box.success::before {
        content: "✅";
    }
    
    .info-box p {
        margin-bottom: 0;
        font-size: 1rem;
    }
    
    /* Streamlit element styling */
    .css-1y4p8pa {
        margin-top: 0 !important;
        padding-top: 3rem !important;
        padding-bottom: 3rem !important;
    }
    
    /* Make st buttons more professional */
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
    
    /* Improve streamlit info/success/warning boxes */
    .stAlert {
        border-radius: 8px;
        box-shadow: 0 2px 8px var(--shadow);
        padding: 1rem !important;
    }
    
    .stAlert > div {
        padding: 0.5rem !important;
    }
    
    /* Fix text color in tabs */
    .stTabs [data-baseweb="tab"] {
        color: var(--text-primary) !important;
        font-weight: 600;
        font-size: 1rem;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        border-bottom-color: var(--border) !important;
    }
    
    .stTabs [aria-selected="true"] {
        color: var(--primary) !important;
        border-bottom-color: var(--primary) !important;
    }
    
    /* Enhance Streamlit elements */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
    }
    
    /* Better text rendering */
    * {
        -webkit-font-smoothing: antialiased;
        -moz-osx-font-smoothing: grayscale;
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
    
    .title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 2rem;
        color: var(--text-primary);
    }
    
    .card {
        background-color: white;
        border-radius: 8px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    </style>
""", unsafe_allow_html=True)

# Navigation Bar with logo
st.markdown("""
<div class="navbar">
    <div class="navbar-logo">
        <span class="navbar-logo-text">Document AI Assistant</span>
    </div>
    <div class="navbar-links">
        <a href="/" class="nav-button" style="background-color: var(--primary-dark);">🏠 Home</a>
        <a href="/documentQuery" class="nav-button">💬 Chat</a>
        <a href="/fileUploader" class="nav-button">📤 Upload</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Main Content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('''
<div style="position: relative; z-index: 2; display: flex; align-items: center;">
    <div style="flex: 3;">
        <h1>Document AI Assistant</h1>
        <p>Interact with your documents using advanced AI technology</p>
    </div>
    <div style="flex: 1; text-align: right;">
        <img src="https://cdn-icons-png.flaticon.com/512/2103/2103633.png" style="max-width: 100px; border-radius: 8px;">
    </div>
</div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Features section with cards
col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class="card">
        <h2>💬 Chat with Documents</h2>
        <p>Upload documents and engage in intelligent conversations about their content. Get instant answers and insights from your documents.</p>
        <a href="/documentQuery" style="text-decoration: none;">
            <button style="
                background-color: var(--primary);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.7rem 1.25rem;
                font-weight: 600;
                width: 100%;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 1rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                Start Chatting
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <h2>📤 Upload Documents</h2>
        <p>Easily upload your documents in various formats including PDF, TXT, and more. Your documents will be processed for intelligent querying.</p>
        <a href="/fileUploader" style="text-decoration: none;">
            <button style="
                background-color: var(--primary);
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.7rem 1.25rem;
                font-weight: 600;
                width: 100%;
                cursor: pointer;
                font-size: 1rem;
                margin-top: 1rem;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);">
                Upload Documents
            </button>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Add section about cosine similarity
st.markdown("""
<div class="content-section" style="margin-top: 2rem;">
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
        <div>
            <h2 style="margin-top: 0; margin-bottom: 0.5rem;">Advanced Document Retrieval</h2>
            <p style="margin-bottom: 0;">Powered by vector similarity search technology</p>
        </div>
        <div style="text-align: right;">
            <img src="https://cdn-icons-png.flaticon.com/512/9529/9529256.png" style="width: 48px; height: 48px; opacity: 0.8;">
        </div>
    </div>
    
    <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-top: 1.5rem;">
        <div style="background-color: white; padding: 1.5rem; border-radius: 8px; border-top: 3px solid var(--primary); box-shadow: 0 4px 12px var(--shadow);">
            <h3 style="color: var(--primary); margin-top: 0;">Cosine Similarity Matching</h3>
            <p>Our system uses cosine similarity to find and retrieve documents that are semantically similar to your queries. This advanced technique measures the cosine of the angle between vectors, ensuring more accurate and relevant results.</p>
        </div>
        
        <div style="background-color: white; padding: 1.5rem; border-radius: 8px; border-top: 3px solid var(--info); box-shadow: 0 4px 12px var(--shadow);">
            <h3 style="color: var(--info); margin-top: 0;">Vector Database Storage</h3>
            <p>Documents are transformed into high-dimensional vectors and stored in an efficient vector database. When you ask questions, your query is matched with existing vectorized documents to retrieve the most relevant information.</p>
        </div>
    </div>
    
    <div style="background-color: rgba(44,82,130,0.03); padding: 1.5rem; border-radius: 8px; margin-top: 1.5rem; display: flex; align-items: center;">
        <div style="margin-right: 1.5rem; flex-shrink: 0;">
            <img src="https://cdn-icons-png.flaticon.com/512/1048/1048966.png" style="width: 40px; height: 40px; opacity: 0.7;">
        </div>
        <p style="margin-bottom: 0;">This approach enables the system to understand the semantic meaning of your questions and find documents with similar context, even if they don't contain the exact same keywords.</p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)