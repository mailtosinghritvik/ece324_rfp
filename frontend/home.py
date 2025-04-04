import streamlit as st
import os

# Set page configuration
st.set_page_config(
    page_title="Welcome to RFP Bot!",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS for enhanced styling
st.markdown("""
    <style>
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
    </style>
""", unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.success("Select a demo above.")

# Main content
st.markdown('<h1 class="main-header">Welcome to RFP Bot 🤖</h1>', unsafe_allow_html=True)

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
            Use the navigation menu on the left to access different features.
        </p>
    </div>
""", unsafe_allow_html=True)

# Add footer
st.markdown("""
    <div style='text-align: center; padding: 20px 0; color: #666; font-size: 0.9em; margin-top: 40px;'>
        Powered by Advanced AI Technology 🚀
    </div>
""", unsafe_allow_html=True)