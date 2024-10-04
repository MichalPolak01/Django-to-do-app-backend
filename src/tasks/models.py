from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class TaskEntryModel(models.Model):
    STATUS_CHOICES = [
        ("BACKLOG", "Backlog"),
        ("SPRINT", "Sprint"),
        ("TODAY", "Today"),
        ("IN_PROGRESS", "In progress"),
        ("COMPLETED", "Completed")
    ]

    IMPORTANCE_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="BACKLOG")
    estimated_time = models.DurationField(default="1:00:00")
    execution_time = models.DurationField(default="0:00:00")
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default="LOW")