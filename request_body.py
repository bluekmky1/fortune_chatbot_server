from pydantic import BaseModel
from typing import Optional, Dict


class Intent(BaseModel):
    id: str
    name: str


class Block(BaseModel):
    id: str
    name: str


class User(BaseModel):
    id: str
    type: str
    properties: Dict[str, str]


class UserRequest(BaseModel):
    timezone: str
    params: Dict[str, str]
    block: Block
    utterance: str
    lang: Optional[str] = None
    user: User


class Bot(BaseModel):
    id: str
    name: str


class Action(BaseModel):
    name: str
    clientExtra: Optional[str] = None
    params: Dict[str, str]
    id: str


class RequestBody(BaseModel):
    intent: Intent
    userRequest: UserRequest
    bot: Bot
    action: Action
