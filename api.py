from flask import Flask, request, jsonify, send_file, after_this_request
from openai import OpenAI
import shutil
import glob
import time
import os
import yaml
import argparse
import sys
from datetime import datetime  # Import datetime module

app = Flask(__name__)

UPLOAD_FOLDER = 'temp'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

threads = {}  # Dictionary to store thread instances with their names

# Initialize OpenAI client at the global scope
client = OpenAI()

@app.route('/uploadFile', methods=['POST'])
def upload_file():
    # Check if the file is in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    # Check if a file was uploaded
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Check if the file is a PDF
    if not file.filename.endswith('.pdf'):
        return jsonify({"error": "Only PDF files are allowed"}), 400

    # Save the uploaded file temporarily
    temp_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(temp_path)

    try:
        # Upload the file to the assistant’s vector store
        assistant = client.beta.assistants.retrieve("asst_Wk1Ue0iDYkhbdiXXDPPJsvAV")

        with open(temp_path, "rb") as f:
            file_batch = client.beta.vector_stores.file_batches.upload_and_poll(
                vector_store_id='vs_qUspcB7VllWXM4z7aAEdIK9L', files=[f]
            )

        # Check upload status
        if file_batch.status != "completed":
            return jsonify({"error": "File upload failed"}), 500

        # Clean up the temporary file after upload
        os.remove(temp_path)

        return jsonify({"response": "File uploaded successfully"}), 200
    
    except Exception as e:
        # Handle exceptions and send a response
        return jsonify({"error": str(e)}), 500


@app.route('/threads', methods=['GET', 'POST'])
def manage_threads():
    if request.method == 'GET':
        # Return the list of threads with IDs and names
        thread_list = [{'id': thread_id, 'name': info['name']} for thread_id, info in threads.items()]
        return jsonify({"threads": thread_list}), 200
    elif request.method == 'POST':
        # Get thread name from request body
        data = request.get_json()
        thread_name = data.get('name')
        # Set default name to "Thread [DATETIME]" if name is not provided or empty
        if not thread_name or thread_name.strip() == '':
            thread_name = f"Thread {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        # Create a new thread using the OpenAI API
        thread = client.beta.threads.create()
        # Store the thread along with its name
        threads[thread.id] = {'thread': thread, 'name': thread_name}
        return jsonify({"thread_id": thread.id, "name": thread_name}), 201

@app.route('/threads/<thread_id>', methods=['DELETE'])
def delete_thread(thread_id):
    if thread_id in threads:
        del threads[thread_id]
        return jsonify({"message": "Thread deleted"}), 200
    else:
        return jsonify({"error": "Thread not found"}), 404

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json
    question = data.get('question')
    thread_id = data.get('thread_id')

    if not question or not thread_id:
        return jsonify({"error": "Question and Thread ID are required"}), 400
    if thread_id not in threads:
        return jsonify({"error": "Thread not found"}), 404

    thread = threads[thread_id]['thread']

    try:
        assistant = client.beta.assistants.retrieve("asst_Wk1Ue0iDYkhbdiXXDPPJsvAV")

        # Create a message in the existing thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=question
        )

        # Run the assistant and get the response
        run = client.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant.id,
        )

        messages = client.beta.threads.messages.list(thread_id=thread.id)
        assistant_reply = messages.data[0].content[0].text.value
        
        if assistant_reply:
            return jsonify({"response": assistant_reply}), 200
        else:
            return jsonify({"error": "Assistant did not provide a response."}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5500, debug=True)  # Added debug=True for more detailed logs
