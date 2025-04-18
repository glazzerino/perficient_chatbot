from pydantic import BaseModel


class Payload(BaseModel):
    prompt: str
    context: dict
    auth: dict
