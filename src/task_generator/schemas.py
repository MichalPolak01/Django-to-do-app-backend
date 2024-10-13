from pydantic import BaseModel


class TaskInput(BaseModel):
    topic: str