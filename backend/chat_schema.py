from pydantic import BaseModel, Field, ValidationError
from typing import List, Any, Union, Optional, Dict
from datetime import datetime
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
    
# TODO: Delete
class ChatHistory(BaseModel):
    chats: List[Chat] = Field(default_factory=list)
    

class ChatManager(BaseModel):
    chats: Dict[str, Chat] = Field(default_factory=dict)
    
    def add_chat(self, chat: Chat):
        """Adds a new chat to the chat manager"""
        self.chats[chat.sessionId] = chat
        
    def get_chat(self, session_id: str) -> Chat:
        """Retrieves a chat by its session ID"""
        return self.chats.get(session_id)
        
    def delete_chats(self, session_ids: List[str]):
        """Deletes chats for the given session IDs"""
        for session_id in session_ids:
            self.chats.pop(session_id)
            
    def load_chats(self, filename: str):
        """Load the chats from the given filename"""
        try:
            with open(filename, "r", encoding="utf-8") as file:
                raw_data = file.read()
                parsed_manager = ChatManager.model_validate_json(raw_data)
                self.chats = parsed_manager.chats
        except ValidationError as e:
            self.chats = {}
            print(e)


def to_json(data: Union[BaseModel, List[BaseModel]], include: Optional[Dict[str, Any]] = None, exclude: Optional[Dict[str, Any]] = None) -> Any:
    """
    Converts a Pydantic BaseModel instance or a list of BaseModel instances into JSON-serializable format,
    with the option to exclude specified fields.

    Args:
        data: A Pydantic BaseModel instance or a list of BaseModel instances.
        include (Optional[Dict[str, Any]]): Fields to include (set True for fields you want).
        exclude (Optional[Dict[str, Any]]): Fields to exclude (set True for fields you want to omit).

    Returns:
        A JSON-serializable dictionary or list of dictionaries.
    """
    if isinstance(data, BaseModel):
        return data.model_dump(include=include, exclude=exclude)  # Convert a single BaseModel to a dictionary with exclusions
    elif isinstance(data, list):
        return [item.model_dump(include=include, exclude=exclude) for item in data if isinstance(item, BaseModel)]  # Convert a list of BaseModel
    else:
        raise TypeError("Input must be a Pydantic BaseModel or a list of BaseModel instances.")
