from pydantic import BaseModel
from typing import Literal, List, Dict, Any, Optional


class Tool(BaseModel):
    Name: str


class ToolCallFunction(BaseModel):
    name: str
    arguments: Dict[str, Any]


class ToolCall(BaseModel):
    id: str
    type: Literal["function"]
    function: ToolCallFunction


class ChatMessage(BaseModel):
    role: Literal["system", "user", "assistant"]
    content: str
    tool_calls: Optional[List[ToolCall]] = None


class Choice(BaseModel):
    model: str
    message: ChatMessage


class ChatCompletion(BaseModel):
    choices: List[Choice]


class ApiKeys(BaseModel):
    openai: str
    groq: str
    anthropic: str
    google: str
    cohere: str


class DialtoneClient(BaseModel):
    api_keys: ApiKeys
