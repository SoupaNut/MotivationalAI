from pydantic import BaseModel, Field, ValidationError
from typing import List, Any, Dict
from datetime import datetime
from google.cloud import storage
from google.oauth2.service_account import Credentials
import uuid

class Message(BaseModel):
    role: str
    parts: List[str] = Field(default_factory=list)
    
class Chat(BaseModel):
    """Create a Chat object that on init, will create a new session ID"""
    sessionId: str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: str = Field(default_factory=lambda: datetime(1,1,1,0,0).isoformat() + "Z")
    history: List[Message] = Field(default_factory=list)
    summary: str = ""
    
    def get_history(self) -> List[Dict[str, Any]]:
        """
        Retrieve the chat history as a list of JSON objects.
        
        Returns:
            List[Dict[str, Any]]: A list of JSON objects representing each message in the history.
        """
        return [message.model_dump() for message in self.history]
    
    def set_summary(self, summary: str):
        """Set the summary in the chat"""
        self.summary = summary
        
    def add_message(self, message: Message):
        """Adds a message to the chat by appending to the history and updating the timestamp"""
        self.history.append(message)
        self.timestamp = datetime.now().isoformat() + "Z"
    

class ChatManager(BaseModel):
    chats: Dict[str, Chat] = Field(default_factory=dict)
    
    def add_chat(self, chat: Chat):
        """Adds a new chat to the chat manager"""
        self.chats[chat.sessionId] = chat
        
    def get_chat(self, session_id: str) -> Chat:
        """Retrieves a chat by its session ID"""
        return self.chats.get(session_id)
        
    def delete_chats(self, session_ids: List[str]):
        """Deletes chats for the given session IDs. Returns a list of successfully deleted chats"""
        chats_deleted = []
        for session_id in session_ids:
            try:
                self.chats.pop(session_id)
                chats_deleted.append(session_id)
            except KeyError:
                return chats_deleted
            
        return chats_deleted
    
    def load_chats(self, bucket_name: str, file_path: str, service_account_key_path: str):
        """
        Load the chats from a file stored in Google Cloud Storage.

        Args:
            bucket_name (str): The name of the GCS bucket.
            file_path (str): The path to the file in the GCS bucket.
            service_account_key_path (str): Path to the service account key file for authentication.
        """
        try:
            blob = self.__get_gc_blob(bucket_name, file_path, service_account_key_path)
            
            # download the file content as a string
            raw_data = blob.download_as_text(encoding="utf-8")
            
            parsed_manager = ChatManager.model_validate_json(raw_data)
            self.chats = parsed_manager.chats
            
        except ValidationError as e:
            self.chats = {}
            print("Validation Error: ", e)
        except Exception as e:
            self.chats = {}
            print("Error loading chats from GCS: ", e)
            
    def save_chats(self, bucket_name: str, file_path: str, service_account_key_path: str):
        """
        Save the current chats to a file in Google Cloud Storage.

        Args:
            bucket_name (str): The name of the GCS bucket.
            file_path (str): The path to the file in the GCS bucket.
            service_account_key_path (str): Path to the service account key file for authentication.
        """
        try:
            blob = self.__get_gc_blob(bucket_name, file_path, service_account_key_path)
            data = self.model_dump_json(indent=4)
            
            blob.upload_from_string(data, content_type="application/json")
            
            print(f"Chats saved successfully to {file_path} in bucket {bucket_name}.")
            
        except Exception as e:
            self.chats = {}
            print("Error saving chats to GCS: ", e)
    
    
    def __get_gc_blob(self, bucket_name: str, file_path: str, service_account_key_path: str):
        """
        Helper function that gets and returns the blob at the given bucket, file path, and service account key.

        Args:
            bucket_name (str): The name of the GCS bucket.
            file_path (str): The path to the file in the GCS bucket.
            service_account_key_path (str): Path to the service account key file for authentication.
        """
        # Create credentials from the service account key file
        credentials = Credentials.from_service_account_file(service_account_key_path)

        # Create storage client using the provided credentials
        # client = storage.Client()
        client = storage.Client(credentials=credentials)
        
        # get bucket with name
        bucket = client.get_bucket(bucket_name)
        
        # get the blob
        blob = bucket.get_blob(file_path)
        
        return blob
