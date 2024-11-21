from pydantic import BaseModel, Field
from typing import List, Any, Union, Optional, Dict
from datetime import datetime

class Message(BaseModel):
    role: str
    parts: List[str] = Field(default_factory=list)
    
class Chat(BaseModel):
    sessionId: str
    timestamp: str = Field(default_factory=lambda: datetime(1,1,1,0,0).isoformat() + "Z")
    history: List[Message] = Field(default_factory=list)
    summary: str
    
class ChatHistory(BaseModel):
    chats: List[Chat] = Field(default_factory=list)
    


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
