import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import os
import json
import uuid

MODEL_NAME = "gemini-1.5-flash"
CONFIG_FILE = "model_config.txt"
GENERATE_SUMMARY_PROMPT_FILE = "summary_prompt.txt"
CHAT_HISTORY_FILE = "current_chat_history.json"
TIMEOUT_DURATION = 10 #seconds

# get api key
load_dotenv('.env')
genai.configure(api_key=os.getenv("API_KEY"))

# Create the model
generation_config = {
  "temperature": 2,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 150,
  "response_mime_type": "text/plain",
}
# this is in json. so is generation_config
safety_settings={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
}

with open(CONFIG_FILE, "r") as file:
    content = file.read()
    model = genai.GenerativeModel(
        model_name=MODEL_NAME, 
        system_instruction=content, 
        generation_config=generation_config, 
        safety_settings=safety_settings
    )

# Initialize flask app
app = Flask(__name__)

# empty initial chat history
current_chat_history = []

current_chat_session = model.start_chat(history=current_chat_history)

def save_chat_history(session_id, current_chat_history):
    try:
        with open(CHAT_HISTORY_FILE, "r") as file:
            all_histories = json.load(file)
    except(FileNotFoundError, json.JSONDecodeError):
        all_histories = {}

    summary = generate_summary()

    all_histories[session_id] = {"history": current_chat_history, "summary": summary};

    with open(CHAT_HISTORY_FILE, "w") as file:
        json.dump(all_histories, file)

# generates summary of the current chat session
def generate_summary() -> str:
    response = current_chat_session.send_message("Summarize this conversation in less than 5 words.")
    return response.text.strip()
        

@app.route("/api/gemini/request", methods=['POST'])
def handle_user_request():
    global current_chat_session, current_chat_history
    try:
        data = request.json
        user_input = data.get("prompt", "")

        if not user_input:
            return jsonify({"response": "Prompt is required"}), 400
        
        current_chat_history.append({"role": "user", "parts": [user_input]})
        response = current_chat_session.send_message(user_input)
        current_chat_history.append({"role": "model", "parts": [response.text]})

        cleaned_text = response.text.rstrip() # remove white space at the end, since gemini seems to add extra newlines
        return jsonify({"response": cleaned_text}), 200

    except Exception as e:
        return jsonify({"response": str(e)}), 500

# @app.route("/api/gemini/create_session", methods=['POST'])
# def create_session():
#     session_id = str(uuid.uuid4())
#     return jsonify({"session_id": session_id})

@app.route("/api/gemini/new", methods=['POST'])
def start_new_chat():
    global current_chat_session, current_chat_history
    save_chat_history() # TODO: add session id and chat history
    try:
        data = request.json

        current_chat_history = data.get("history", []);

        current_chat_session = model.start_chat(history=current_chat_history)

        return jsonify({"response": ""}), 200

    except Exception as e:
        return jsonify({"response": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True); # for testing and debugging
    # app.run(host="0.0.0.0", port=8080) # google expects app to run on port 8080