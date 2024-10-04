from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404, get_list_or_404
from django.forms.models import model_to_dict

from .schemas import TaskCreateSchema, TaskDetailSchema, TaskUpdateSchema, MessageSchema, ErrorTaskUpdateSchema, TaskExecutionTimeUpdateSchema
from .models import TaskEntryModel
from .forms import TaskForm
import helpers
import json

router = Router()


@router.post("", response={201: TaskDetailSchema, 400: ErrorTaskUpdateSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def create_task(request, payload: TaskCreateSchema):  
    form = TaskForm(data=payload.dict(), instance=TaskEntryModel(user=request.user))

    if form.is_valid():
        task = form.save(commit=False)
        task.user = request.user
        task.save()

        task_data = format_task_time(task)

        return 201, task_data
    else:
         form_errors = json.loads(form.errors.as_json())
         return 400, form_errors


@router.get("", response={200: List[TaskDetailSchema]}, auth=helpers.api_auth_required, tags=["Tasks"])
def get_tasks(request):  
    tasks = get_list_or_404(TaskEntryModel, user=request.user)
    task_list = []

    for task in tasks:
        task_data = format_task_time(task)

        task_list.append(task_data)

    return 200, task_list


@router.get("{id}", response={200: TaskDetailSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def get_task(request, id:int):
    task = get_object_or_404(TaskEntryModel, id=id, user=request.user)    
    
    task_data = format_task_time(task)
    
    return 200, task_data


@router.put("{id}", response={200: TaskDetailSchema, 400: ErrorTaskUpdateSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def update_task(request, payload: TaskUpdateSchema, id: int):
    task = get_object_or_404(TaskEntryModel, id=id, user=request.user)

    form = TaskForm(payload.dict(), instance=task)

    if form.is_valid():
        task = form.save()

        task_data = format_task_time(task)

        return 200, task_data
    else:
        form_errors = json.loads(form.errors.as_json())
        return 400, form_errors


@router.put("in-progress/add-execution-time", response={200: TaskDetailSchema, 400: MessageSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def add_execution_time(request, payload: TaskExecutionTimeUpdateSchema):

    try:
        task = TaskEntryModel.objects.get(user=request.user, status="IN_PROGRESS")

        task.execution_time += payload.execution_time
        task.save()

        task_data = format_task_time(task)
        return 200, task_data

    except TaskEntryModel.DoesNotExist:
        return 400, {"message": "There are no in progress task."}


@router.delete("{id}", response={204: MessageSchema}, auth=helpers.api_auth_required, tags=["Tasks"])
def delete_task(request, id: int):
    task = get_object_or_404(TaskEntryModel, id=id, user=request.user)

    task.delete()
    return 204, {"message": "Task deleted successfully."}


def format_task_time(task):
    task_data = model_to_dict(task)

    estimated_hours, estimated_minutes, estimated_seconds = str(task.estimated_time).split(":")
    task_data['estimated_time'] = f"{estimated_hours.zfill(2)}:{estimated_minutes.zfill(2)}:{estimated_seconds.zfill(2)}"

    execution_hours, execution_minutes, execution_seconds = str(task.execution_time).split(":")
    task_data['execution_time'] = f"{execution_hours.zfill(2)}:{execution_minutes.zfill(2)}:{execution_seconds.zfill(2)}"


    return task_data