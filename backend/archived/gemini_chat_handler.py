import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
from datetime import datetime
from pydantic import ValidationError
from chat_schema import *
import os
import json
import uuid

# constants
MODEL_NAME = "gemini-1.5-flash"
CONFIG_FILE = "model_config.txt"
GENERATE_SUMMARY_PROMPT_FILE = "summary_prompt.txt"
CHAT_HISTORY_FILE = "chat_history.json"
TIMEOUT_DURATION = 10 #seconds


class GeminiChatHandler:
    def __init__(self):
        self.config_api_key()
        self.model = self.init_model()
        self.chat_session = self.model.start_chat(history=[])
        self.session_id = str(uuid.uuid4())
        self.all_chats = self.load_all_chats()

        # self.start_new_chat() # init chat session and session id

    @staticmethod
    def config_api_key():
        load_dotenv(".env")
        api_key = os.getenv("API_KEY")
        if api_key:
            genai.configure(api_key=api_key)
        else:
            raise ValueError("API_KEY not found in environment variables.")
    
    @staticmethod
    def init_model():
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
                raw_data = json.load(file)
                chat_history = ChatHistory(**raw_data) # validate and parse
                return chat_history.chats
            
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        except ValidationError as e:
            print(f"Validation error: {e.json()}")
            return []
        
    def start_new_chat(self) -> tuple[str, int]:
        try:
            # don't do anything if current session is not saved in all_chats
            # it's only saved if we have sent a message
            # this means the chat history for this session is empty
            old_session_id = self.session_id
            chat = self.find_chat(old_session_id)
            if not chat:
                return old_session_id, 200
            
            # save our current history to file
            self.save_chat_history(old_session_id)

            # generate new session id
            self.session_id = str(uuid.uuid4())

            # start new session
            self.chat_session = self.model.start_chat(history=[])

            return self.session_id, 200
        except Exception as e:
            return str(e), 500

    def load_chat(self, session_id):
        chat = self.find_chat(session_id)
        if not chat:
            return "Session ID not found", 404
        
        try:
            history = to_json(chat.history)
            self.chat_session = self.model.start_chat(history=history)
            self.session_id = session_id
            
            return to_json(chat), 200
        
        except Exception as e:
            return str(e), 500

    # send user message to model
    def send_message(self, message) -> tuple[str, int]:
        try:
            # find existing chat or create a new one
            chat = self.find_chat(self.session_id)
            if not chat:
                chat = Chat(sessionId=self.session_id)
                self.all_chats.append(chat)

            # add user message
            user_message = Message(role="user", parts=[message])
            chat.history.append(user_message)
            
            print("Before: ", chat)
            
            # send message to model
            response = self.chat_session.send_message(message)
            cleaned_text = response.text.rstrip() # remove white space at the end, since gemini seems to add extra newlines

            # add model response
            model_message = Message(role="model", parts=[response])
            chat.history.append(model_message)

            chat.timestamp = datetime.now().isoformat() + "Z"
            
            print("After: ", chat)
            
            return cleaned_text, 200
        
        except Exception as e:
            return str(e), 500
        

    # returns summary of the current chat session
    def generate_summary(self) -> str:
        response = self.chat_session.send_message("Summarize this conversation in less than 5 words. Don't use emojis or punctuation. Write the summary in title case.")
        return response.text.strip()
    
    def save_chat_history(self, session_id):
        chat = self.find_chat(session_id)
        # print(type(self.all_chats))
        if chat:
            summary = self.generate_summary()
            chat.summary = summary

            with open(CHAT_HISTORY_FILE, "w") as file:
                chat_objects: List[Chat] = [Chat(**chat) for chat in self.all_chats]
                chat_history = ChatHistory(chat_objects);
                
                # json.dump(to_json(chats), file, indent=4)
                json.dump(to_json(chat_history), file, indent=4)
                

    def get_all_chats(self):
        return self.all_chats
    
    def get_current_session_id(self):
        return self.session_id
    
    # helper function
    def find_chat(self, session_id):
        for chat in self.all_chats:
            if chat.sessionId == session_id:
                return chat
        return None
