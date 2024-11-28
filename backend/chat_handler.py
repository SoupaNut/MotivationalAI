import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import os
import json
from chat_schema import *

MODEL_NAME = "gemini-1.5-flash"
CONFIG_FILE = "model_config.txt"
GENERATE_SUMMARY_PROMPT_FILE = "summary_prompt.txt"
CHAT_HISTORY_FILE = "history.json"
TIMEOUT_DURATION = 10 #seconds

class GeminiChatHandler:
    def __init__(self):
        self.config_api_key()
        self.model = self.init_model()
        self.chat_session = self.model.start_chat(history=[])
        self.all_chats = ChatManager()
        self.all_chats.load_chats(CHAT_HISTORY_FILE)
        self.current_chat = Chat()
        
        
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
            "top_k": 40,
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
        
        
    def start_new_chat(self) -> tuple[str, int]:
        """
        Starts a new chat and chat session. If the current chat has no history, nothing will be done and the current chat session ID will be returned.
        If there is history, then a summary will be generated based on the given history and the current chat will be saved and added to all chats.
        
        Returns: 
            - (str) session ID
            - (int) status code
        """
        try:
            # return current chat if history is empty
            if not self.current_chat.history:
                return self.current_chat.sessionId, 200
            
            # generate a summary for the current chat
            # print("generate summary")
            response = self.chat_session.send_message("Summarize this conversation in less than 5 words. Don't use emojis or punctuation. Write the summary in title case.")
            self.current_chat.set_summary(response.text.strip())
            
            # add current chat to all_chats and save to file
            # print("add current chat")
            self.all_chats.add_chat(self.current_chat)
            self.save_chats_to_file()
            
            # create new chat and session, and return its session ID
            # print("create new chat")
            self.current_chat = Chat()
            self.chat_session = self.model.start_chat(history=[])
            return self.current_chat.sessionId, 200
            
        except Exception as e:
            return str(e), 500
        
    
    def load_chat(self, session_id: str):
        """
        Starts a new chat with the provided session ID. Loads the model with the session's history.
        Returns a json object of the current chat if succeeds.
        """
        chat = self.all_chats.get_chat(session_id)
        
        if not chat:
            self.current_chat = Chat(sessionId=session_id)
            return "Session ID not found. Creating new Chat with the provided session ID", 404
        
        try:
            # convert chat's history to json, start the model with the provided history, and set current chat to this
            history = chat.get_history()
            self.chat_session = self.model.start_chat(history=history)
            self.current_chat = chat
            
            return self.current_chat.model_dump(), 200
        
        except Exception as e:
            return str(e), 500
        
    
    def delete_chats(self, session_ids: List[str]):
        """
        Deletes chats based on the given session IDs
        """
        chats_deleted = self.all_chats.delete_chats(session_ids)
        self.save_chats_to_file()
        
        if len(chats_deleted) != len(session_ids):
            return chats_deleted, 404
        else:
            return chats_deleted, 200
        
    
    
    def send_message(self, message: str) -> tuple[str, int]:
        """
        Send a message to the model and get a response.
        
        Returns: 
            - (str) model's response string
            - (int) status code
        """
        if not message: 
            return "Message cannot be empty", 400
        
        try:
            # Add current chat to all_chats if it's not there already
            chat = self.all_chats.get_chat(self.current_chat.sessionId)
            if not chat:
                self.all_chats.add_chat(self.current_chat)
                chat = self.current_chat
            
            # add user message
            user_message = Message(role="user", parts=[message])
            chat.add_message(user_message)
            
            # send message to model
            response = self.chat_session.send_message(message)
            cleaned_text = response.text.rstrip() # remove white space at the end, since gemini seems to add extra newlines
            
            # add model response
            model_message = Message(role="model", parts=[cleaned_text])
            chat.add_message(model_message)
            
            return cleaned_text, 200
        
        except Exception as e:
            return str(e), 500
        
    
    def save_chats_to_file(self, filename: str=CHAT_HISTORY_FILE):
        """Write all_chats to the provided filename"""
        
        # explicitly specify UTF-8 encoding since python on some systems might use a different encoding that doesn't support emojis
        with open(filename, "w", encoding="utf-8") as file:
            data = self.all_chats.model_dump()
            
            # ensure_ascii ensures emojis and other non-ASCII characters are written directly in JSON, instead of being escaped
            json_data = json.dumps(data, indent=4, ensure_ascii=False) 
            file.write(json_data)
            
            
    def get_current_session_id(self) -> str:
        """gets the session id for the current chat"""
        return self.current_chat.sessionId
    
    
    def get_all_chats(self) -> ChatManager:
        """Gets all chats and returns a ChatManager object"""
        return self.all_chats
    
    # TODO: Is this needed?
    def close_handler(self):
        """
        Looks at self.all_chats and compares each chat's timestamp. If the timestamp is more recent than the one in the file and the summary is the same,
        then update the summary of that chat. Lastly, save self.all_chats to the file.
        """
        # read the history in the file
        stored_data = ChatManager()
        stored_data.load_chats()
        
        for session_id, chat in self.all_chats.chats.items():
            stored_chat = stored_data.get_chat(session_id) # TODO: what happens when it's a new chat that has history but isn't in the file?
            
            # Define the format for ISO 8601 with microseconds and 'Z'
            format = "%Y-%m-%dT%H:%M:%S.%fZ"
            
            # convert strings to datetime objects
            current_time = datetime.strptime(chat.timestamp, format)
            stored_time = datetime.strptime(stored_chat.timestamp, format)
            
            # generate a new summary if the current timestamp is more recent and the summaries are the same
            same_summary = chat.summary == stored_chat.summary
            if (current_time > stored_time) and same_summary:
                print(f"genertae summary: {chat.summary}")
                
        return "", 200 #TODO: delete
            
            
            
                