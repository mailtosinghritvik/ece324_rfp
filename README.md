# RFP Bot

A chatbot application for processing and querying Request for Proposal (RFP) documents.

## Project Structure

- `frontend/`: Streamlit-based web interface
- `backend/`: Flask API and data processing logic

## Setup Instructions

### Backend Setup

1. Create a virtual environment:
   ```bash
   python -m venv openai-env
   ```

2. Activate the virtual environment:
   - Windows:
     ```bash
     .\openai-env\Scripts\activate
     ```
   - Mac/Linux:
     ```bash
     source openai-env/bin/activate
     ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the backend API:
   ```bash
   cd backend
   python api.py
   ```

### Frontend Setup

1. Ensure the virtual environment is activated (see step 2 above)

2. Run the Streamlit application:
   ```bash
   cd frontend
   streamlit run home.py
   ```

## Features

- Document upload and processing
- Query-based interaction with documents
- Thread-based conversation memory
