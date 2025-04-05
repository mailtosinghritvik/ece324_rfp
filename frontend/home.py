import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="Welcome to RFP Bot!",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for enhanced styling - including hiding the sidebar
st.markdown("""
    <style>
    /* Hide sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    
    .main-header {
        font-size: 3.5em;
        background: linear-gradient(45deg, #2E3192, #1BFFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 20px 0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .feature-card {
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #e0e0e0;
        background: white;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin: 10px;
        transition: transform 0.3s ease;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
    }
    
    .feature-icon {
        font-size: 2em;
        margin-bottom: 10px;
    }
    
    .feature-title {
        font-size: 1.5em;
        margin-bottom: 10px;
        color: #2E3192;
    }
    
    .feature-description {
        color: #666;
        line-height: 1.6;
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
        <a href="/" class="nav-item active">
            <span class="nav-icon">🏠</span>Home
        </a>
        <a href="/documentQuery" class="nav-item">
            <span class="nav-icon">📝</span>Document Query
        </a>
        <a href="/fileUploader" class="nav-item">
            <span class="nav-icon">📤</span>File Uploader
        </a>
    </div>
""", unsafe_allow_html=True)

# Main content
st.markdown('<h1 class="main-header">Welcome to RFP Bot 🤖</h1>',
            unsafe_allow_html=True)

# Subtitle
st.markdown("""
    <div style='text-align: center; padding: 20px 0; font-size: 1.5em; color: #666;'>
        Your Intelligent Assistant for RFP Analysis and Management
    </div>
""", unsafe_allow_html=True)

# Create three columns for feature cards
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">📄</div>
            <div class="feature-title">Document Processing</div>
            <div class="feature-description">
                Efficiently process and analyze RFP documents with advanced AI technology.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">🔍</div>
            <div class="feature-title">Smart Search</div>
            <div class="feature-description">
                Quickly find relevant information with our intelligent search capabilities.
            </div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
        <div class="feature-card">
            <div class="feature-icon">💡</div>
            <div class="feature-title">AI-Powered Insights</div>
            <div class="feature-description">
                Get valuable insights and recommendations from your RFP documents.
            </div>
        </div>
    """, unsafe_allow_html=True)

# Add a getting started section
st.markdown("""
    <div style='text-align: center; padding: 40px 0; margin-top: 40px;'>
        <h2 style='color: #2E3192; margin-bottom: 20px;'>Getting Started</h2>
        <p style='color: #666; font-size: 1.2em; max-width: 800px; margin: 0 auto;'>
            Upload your RFP documents and start exploring with our powerful tools. 
            Use the navigation menu at the top to access different features.
        </p>
    </div>
""", unsafe_allow_html=True)

# Add footer
st.markdown("""
    <div style='text-align: center; padding: 20px 0; color: #666; font-size: 0.9em; margin-top: 40px;'>
        Powered by Advanced AI Technology 🚀
    </div>
""", unsafe_allow_html=True)
