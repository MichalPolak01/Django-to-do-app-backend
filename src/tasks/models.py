from django.db import models
from django.conf import settings


User = settings.AUTH_USER_MODEL

class TaskEntryModel(models.Model):
    STATUS_CHOICES = [
        ("backlog", "Backlog"),
        ("sprint", "Sprint"),
        ("today", "Today"),
        ("in_progress", "In progress"),
        ("completed", "Completed")
    ]

    IMPORTANCE_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=25, choices=STATUS_CHOICES, default="backlog")
    estimated_time = models.DurationField(default="1h")
    execution_time = models.DurationField(null=True, blank=True)
    importance = models.CharField(max_length=20, choices=IMPORTANCE_CHOICES, default="low")