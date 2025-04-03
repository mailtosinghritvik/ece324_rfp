import streamlit as st
import requests
import os
import base64
import socket

# Import the same styling as home page
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

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
    
    /* Card styling with better visibility */
    .content-section {
        background: var(--card-bg);
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        margin-bottom: 2rem;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        position: relative;
    }
    
    /* Upload area styling - enhanced with professional design */
    .upload-area {
        border: 2px dashed var(--border);
        border-radius: 8px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin: 2rem 0;
        transition: all 0.3s ease;
        background-color: rgba(44,82,130,0.03);
        cursor: pointer;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .upload-area:hover {
        border-color: var(--primary);
        background-color: rgba(44,82,130,0.05);
        transform: translateY(-3px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.05);
    }
    
    .upload-area h3 {
        font-size: 1.4rem;
        margin-top: 1.5rem;
        margin-bottom: 0.75rem;
        color: var(--primary);
    }
    
    .upload-area p {
        font-size: 1rem;
        color: var(--text-secondary);
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
    
    /* File list styling - cleaner design */
    .file-list {
        margin-top: 2rem;
        padding: 1.5rem;
        background: rgba(44,82,130,0.03);
        border-radius: 8px;
        border-left: 3px solid var(--primary);
    }
    
    /* Icon styling - professional colors */
    .upload-icon {
        font-size: 4rem;
        color: var(--primary);
        margin-bottom: 1.5rem;
        opacity: 0.8;
    }
    
    /* File details with professional styling */
    .file-details {
        background: white;
        padding: 2rem;
        border-radius: 8px;
        box-shadow: 0 4px 12px var(--shadow);
        margin: 2rem 0;
        border-left: 3px solid var(--info);
    }
    
    .file-detail-row {
        display: flex;
        justify-content: space-between;
        padding: 0.75rem 0;
        border-bottom: 1px solid var(--border);
    }
    
    .file-detail-label {
        font-weight: 600;
        color: var(--text-primary);
        font-size: 1rem;
    }
    
    .file-detail-value {
        color: var(--text-secondary);
        font-size: 1rem;
    }
    
    /* Tip box styling - better contrast */
    .tip-box {
        background: rgba(221,107,32,0.05);
        border-left: 3px solid var(--warning);
        padding: 1.5rem 2rem;
        border-radius: 8px;
        margin: 2rem 0;
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    
    .tip-box h4 {
        color: var(--warning);
        font-weight: 600;
        margin-top: 0;
        font-size: 1.2rem;
        margin-bottom: 1rem;
    }
    
    .tip-box ul {
        margin-bottom: 0;
        padding-left: 1.25rem;
    }
    
    .tip-box li {
        margin-bottom: 0.75rem;
        position: relative;
    }
    
    .tip-box li strong {
        color: var(--text-primary);
        font-weight: 600;
    }
    
    /* Empty state styling with clean design */
    .empty-state {
        text-align: center;
        padding: 3rem 2rem;
        color: var(--text-light);
        background: rgba(44,82,130,0.03);
        border-radius: 8px;
        margin: 1.5rem 0;
    }
    
    /* Progress indicator - professional colors */
    .progress-indicator {
        display: flex;
        margin: 2.5rem 0;
        position: relative;
    }
    
    .progress-step {
        flex: 1;
        text-align: center;
        position: relative;
    }
    
    .progress-step::before {
        content: "";
        height: 2px;
        background-color: var(--border);
        position: absolute;
        top: 15px;
        left: 0;
        right: 0;
        z-index: 0;
    }
    
    .progress-step:first-child::before {
        left: 50%;
    }
    
    .progress-step:last-child::before {
        right: 50%;
    }
    
    .step-number {
        width: 32px;
        height: 32px;
        background: white;
        border: 2px solid var(--border);
        border-radius: 50%;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        position: relative;
        z-index: 1;
        font-weight: 600;
        color: var(--text-secondary);
        margin-bottom: 0.75rem;
        font-size: 0.9rem;
    }
    
    .step-title {
        font-size: 0.9rem;
        font-weight: 500;
        color: var(--text-secondary);
    }
    
    .progress-step.active .step-number {
        background: var(--primary);
        color: white;
        border-color: var(--primary);
        box-shadow: 0 0 0 3px rgba(44,82,130,0.12);
    }
    
    .progress-step.active .step-title {
        color: var(--primary);
        font-weight: 600;
    }
    
    .progress-step.complete .step-number {
        background: var(--success);
        color: white;
        border-color: var(--success);
        box-shadow: 0 0 0 3px rgba(47,133,90,0.12);
    }
    
    /* Section divider - cleaner design */
    .section-divider {
        display: flex;
        align-items: center;
        margin: 2.5rem 0;
        color: var(--text-light);
        font-size: 1rem;
        font-weight: 500;
    }
    
    .section-divider::before,
    .section-divider::after {
        content: "";
        flex: 1;
        height: 1px;
        background: var(--border);
    }
    
    .section-divider::before {
        margin-right: 1.5rem;
    }
    
    .section-divider::after {
        margin-left: 1.5rem;
    }
    
    /* Improve streamlit info/success/warning boxes */
    .stAlert {
        border-radius: 8px;
        box-shadow: 0 2px 8px var(--shadow);
        padding: 1rem !important;
    }
    
    .stAlert > div {
        padding: 0.5rem !important;
        font-size: 1rem;
    }
    
    /* SVG Icon styling - professional colors */
    svg {
        fill: none;
        stroke: var(--primary);
        opacity: 0.65;
        margin-bottom: 1rem;
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
    
    .upload-container {
        max-width: 800px;
        margin: 0 auto;
        padding: 2rem;
        background-color: white;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .upload-header {
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .upload-area {
        border: 2px dashed var(--border);
        border-radius: 8px;
        padding: 2rem;
        text-align: center;
        margin-bottom: 2rem;
        background-color: rgba(44,82,130,0.03);
    }
    
    .upload-area:hover {
        border-color: var(--primary);
        background-color: rgba(44,82,130,0.05);
    }
    
    .file-info {
        background-color: rgba(44,82,130,0.03);
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1rem;
        border-left: 3px solid var(--primary);
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
        <a href="/" class="nav-button">🏠 Home</a>
        <a href="/documentQuery" class="nav-button">💬 Chat</a>
        <a href="/fileUploader" class="nav-button" style="background-color: var(--primary-dark);">📤 Upload</a>
    </div>
</div>
""", unsafe_allow_html=True)

# Main content
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# Main header
st.markdown('<div class="main-header">', unsafe_allow_html=True)
st.markdown('''
<div style="position: relative; z-index: 2; display: flex; align-items: center;">
    <div style="flex: 3;">
        <h1>Upload Documents</h1>
        <p>Upload your PDF files for analysis and querying with AI</p>
    </div>
    <div style="flex: 1; text-align: right;">
        <img src="https://cdn-icons-png.flaticon.com/512/4319/4319077.png" style="max-width: 100px; border-radius: 8px;">
    </div>
</div>
''', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="content-section">
    <h2>File Uploader</h2>
    <p>Select a PDF file to upload for AI-powered document querying</p>
</div>
""", unsafe_allow_html=True)

# File uploader
uploaded_file = st.file_uploader("Choose a PDF file", type=['pdf'])

if uploaded_file is not None:
    st.markdown("""
    <div class="file-info">
        <h3>Selected File</h3>
    """, unsafe_allow_html=True)
    
    st.write(f"Filename: {uploaded_file.name}")
    st.write(f"Size: {uploaded_file.size/1024:.2f} KB")
    
    if st.button("Upload File"):
        with st.spinner("Uploading and processing file..."):
            try:
                files = {"file": uploaded_file}
                response = requests.post(UPLOAD_URL, files=files)
                
                if response.status_code == 200:
                    st.success("File uploaded and processed successfully!")
                    st.markdown("""
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
                            Go to Chat
                        </button>
                    </a>
                    """, unsafe_allow_html=True)
                else:
                    st.error(f"Error uploading file: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Connection error: {str(e)}")
    
    st.markdown("</div>", unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="upload-area">
        <img src="https://cdn-icons-png.flaticon.com/512/2965/2965335.png" style="width: 80px; margin-bottom: 1rem;">
        <h3>Drag & Drop PDF Files Here</h3>
        <p>Click to browse or drag and drop your files</p>
        <p class="text-light" style="font-size: 0.9rem; margin-top: 1rem; color: var(--text-light);">Supported format: PDF</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
    
