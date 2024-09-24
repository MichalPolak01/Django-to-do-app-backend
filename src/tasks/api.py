from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import ValidationError

from .schemas import TaskCreateSchema, TaskDetailSchema, TaskUpdateSchema, MessageSchema
from .models import TaskEntryModel
import helpers

router = Router()


@router.post("", response={201: TaskDetailSchema, 400: MessageSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def create_task(request, payload: TaskCreateSchema):  
    try: 
        obj = TaskEntryModel.objects.create(
            user = request.user,
            **payload.dict(exclude_unset=True)
        )

        return 201, obj
    except ValidationError as error:
        return 400, {"message": str(error)}
    

@router.get("", response={200: List[TaskDetailSchema]}, auth=helpers.api_auth_required, tags=["Tasks"])
def get_tasks(request):  
    tasks = get_list_or_404(TaskEntryModel, user=request.user)
    return 200, tasks


@router.get("{id}", response={200: TaskDetailSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def get_task(request, id:int):
    task = get_object_or_404(TaskEntryModel, id=id, user=request.user)    
    return 200, task


@router.put("{id}", response={200: TaskDetailSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def update_task(request, payload: TaskUpdateSchema, id: int):
    task = get_object_or_404(TaskEntryModel, id=id, user=request.user)

    for attr, value in payload.dict(exclude_unset=True).items():
        setattr(task, attr, value)

    task.save()
    return 200, task


@router.delete("{id}", response={204: MessageSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def delete_task(request, id: int):
    task = get_object_or_404(TaskEntryModel, id=id, user=request.user)

    task.delete()
    return 204, {"message": "Task deleted successfully."}