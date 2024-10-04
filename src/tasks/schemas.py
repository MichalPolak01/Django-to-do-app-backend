from ninja import Schema
from typing import Optional
from datetime import timedelta
from pydantic import BaseModel
from typing import List, Any, Optional


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
    estimated_time: str
    execution_time: str
    importance: str


class TaskUpdateSchema(Schema):
    title: Optional[str] = None
    label: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    estimated_time: Optional[timedelta] = None
    execution_time: Optional[timedelta] = None
    importance: Optional[str] = None


class MessageSchema(Schema):
    message: str
    

class ErrorTaskUpdateSchema(BaseModel):
    status: Optional[List[Any]] = None


class TaskExecutionTimeUpdateSchema(Schema):
    execution_time: timedelta