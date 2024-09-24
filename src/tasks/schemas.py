from ninja import Schema
from typing import Optional
from datetime import timedelta


class TaskCreateSchema(Schema):
    title: str
    label: str
    description: str
    status: str
    estimated_time: timedelta
    execution_time: timedelta
    importance: str


class TaskDetailSchema(Schema):
    id: int 
    title: str
    label: str
    description: str
    status: str
    estimated_time: timedelta
    execution_time: timedelta
    importance: str


class TaskUpdateSchema(Schema):
    title: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    estimated_time: Optional[float] = None
    execution_time: Optional[float] = None
    importance: Optional[str] = None


class MessageSchema(Schema):
    message: str