import requests
from typing import Any
from pydantic import ValidationError, BaseModel
from dialtone.types import (
    ApiKeys,
    ChatCompletion,
    Choice,
    ChatMessage,
    Tool,
    DialtoneClient,
)

BASE_URL = "https://anneal--llm-router-web-fastapi-app.modal.run"


class Completions(BaseModel):
    client: DialtoneClient

    def create(self, messages: list[ChatMessage], tools: list[Tool] = []):
        response = requests.post(
            f"{BASE_URL}/chat/completions",
            json={
                "messages": [message.model_dump() for message in messages],
                "tools": [tool.model_dump() for tool in tools],
                "dials": {"quality": 0.5, "cost": 0.5, "speed": 0},
                "api_keys": self.client.api_keys.model_dump(),
            },
        )

        response_json = response.json()

        print("response_json", response_json)
        return ChatCompletion(
            choices=[
                Choice(
                    model=response_json["used_model"],
                    message=response_json["message"],
                )
            ]
        )


class Chat(BaseModel):
    client: DialtoneClient
    completions: Completions

    def __init__(self, client: DialtoneClient):
        completions = Completions(client=client)
        super().__init__(client=client, completions=completions)


class Dialtone:
    chat: Chat

    def __init__(self, api_keys: ApiKeys | dict[str, Any]):
        try:
            if not isinstance(api_keys, ApiKeys):
                api_keys = ApiKeys(**api_keys)
        except ValidationError as e:
            raise ValueError(f"Invalid api_keys structure: {e}")

        client = DialtoneClient(api_keys=api_keys)
        self.chat = Chat(client=client)
