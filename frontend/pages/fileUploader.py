import streamlit as st
import requests
import os

# Set page config
st.set_page_config(page_title="File Uploader - RFP Bot",
                   page_icon="📄", layout="wide")

# Custom CSS for enhanced styling
st.markdown("""
    <style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Navigation bar styling */
    .navbar {
        display: flex;
        justify-content: center;
        align-items: center;
        background-color: white;
        padding: 15px 30px;
        border-radius: 12px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 20px auto 30px;
        max-width: 800px;
    }
    
    .nav-item {
        padding: 10px 25px;
        margin: 0 15px;
        text-decoration: none;
        color: #2E3192;
        border-radius: 8px;
        font-weight: 600;
        font-size: 16px;
        transition: all 0.3s ease;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .nav-item:hover {
        background-color: #f0f2f6;
        transform: translateY(-2px);
    }
    
    .nav-item.active {
        background-color: #2E3192;
        color: white;
        box-shadow: 0 4px 8px rgba(46, 49, 146, 0.2);
    }
    
    .nav-icon {
        margin-right: 8px;
        font-size: 18px;
    }
    </style>
""", unsafe_allow_html=True)

# Create horizontal navigation bar at the top
st.markdown("""
    <div class="navbar">
        <a href="/" class="nav-item">
            <span class="nav-icon">🏠</span>Home
        </a>
        <a href="/documentQuery" class="nav-item">
            <span class="nav-icon">📝</span>Document Query
        </a>
        <a href="/fileUploader" class="nav-item active">
            <span class="nav-icon">📤</span>File Uploader
        </a>
    </div>
""", unsafe_allow_html=True)

# Flask server URL
UPLOAD_URL = 'http://127.0.0.1:5500/uploadFile'

st.title("PDF Upload Interface")

# File upload section
st.header("Upload a PDF File")

# File uploader component
uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

# Function to upload file to backend server


def upload_file_to_backend(file_path):
    with open(file_path, "rb") as f:
        files = {'file': f}
        response = requests.post(UPLOAD_URL, files=files)
        if response.status_code == 200:
            st.success("File successfully uploaded!")
        else:
            st.error("Failed to upload file.")


if uploaded_file:
    # Check if the uploaded file is a PDF
    if uploaded_file.type == "application/pdf":
        # Save the uploaded file temporarily
        temp_file_path = os.path.join("temp", uploaded_file.name)

        # Ensure the 'temp' directory exists
        os.makedirs(os.path.dirname(temp_file_path), exist_ok=True)

        # Write the file to the specified path
        with open(temp_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Upload file to the backend
        upload_file_to_backend(temp_file_path)

        # Clean up temporary file after upload
        os.remove(temp_file_path)
    else:
        st.error("Only PDF files are allowed. Please upload a valid PDF.")

# Display logo in main content area instead of sidebar
col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    # Construct absolute path to image
    image_path = "rfp_logo.png"

    # Check if file exists before trying to display
    if os.path.exists(image_path):
        st.image(image_path, width=150)
    else:
        st.error("Logo not found")
