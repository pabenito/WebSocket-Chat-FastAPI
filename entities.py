from pydantic import BaseModel


class Email(BaseModel):
    sender: str
    group: str
    message: str
