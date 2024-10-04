from django.contrib import admin
from .models import TaskEntryModel


class TasksAdmin(admin.ModelAdmin):
    list_display = ("title", "label", "status", "estimated_time", "execution_time", "importance")
    list_filter = ("title", "label", "status", "estimated_time", "execution_time", "importance")

admin.site.register(TaskEntryModel, TasksAdmin)