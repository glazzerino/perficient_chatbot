from pydantic import BaseModel


class MessageHistory(BaseModel):
    messages: list[Message]


class Message(BaseModel):
    type: str
    data: MessageContent

    @validator("type")
    def validate_type(cls, type_value):
        if type_value not in ["human", "ai", "system"]:
            raise ValueError("type must be one of human, ai, system")
        return type_value


class MessageContent(BaseModel):
    content: str
    additional_kwargs: dict
