import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
# from flask import Flask, request, jsonify
import os
import json
import uuid

# constants
MODEL_NAME = "gemini-1.5-flash"
CONFIG_FILE = "model_config.txt"
GENERATE_SUMMARY_PROMPT_FILE = "summary_prompt.txt"
CHAT_HISTORY_FILE = "current_chat_history.json"
TIMEOUT_DURATION = 10 #seconds

# Load environment variables
# load_dotenv('.env')
# genai.configure(api_key=os.getenv("API_KEY"))

# # Initialize Flask app
# app = Flask(__name__)

class GeminiChatHandler:
    def __init__(self):
        self.config_api_key()
        self.model = self.initialize_model()
        self.all_chats = self.load_all_chats()
        self.current_chat_history = []
        self.current_chat_session = self.start_new_chat(self, [])

    @staticmethod
    def config_api_key():
        load_dotenv(".env")
        api_key = os.getenv("API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            raise ValueError("API_KEY not found in environment variables.")
    
    @staticmethod
    def initialize_model():
        generation_config = {
            "temperature": 2,
            "top_p": 0.95,
            "top_k": 64,
            "max_output_tokens": 150,
            "response_mime_type": "text/plain",
        }
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }

        with open(CONFIG_FILE, "r") as file:
            system_instruction = file.read()

        return genai.GenerativeModel(
            model_name=MODEL_NAME, 
            system_instruction=system_instruction, 
            generation_config=generation_config, 
            safety_settings=safety_settings
        )

    @staticmethod
    def load_all_chats():
        try:
            with open(CHAT_HISTORY_FILE, "r") as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}
        
    def start_new_chat(self, history=[]):
        session_id = str(uuid.uuid4())
        

# Main entry point
# if __name__ == "__main__":
#     app.run(debug=True)
#     # app.run(host="0.0.0.0", port=8080) # For deployment