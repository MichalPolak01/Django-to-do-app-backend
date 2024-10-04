from django import forms
from datetime import timedelta

from .models import TaskEntryModel

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskEntryModel
        fields = ['title', 'label', 'description', 'status', 'estimated_time', 'execution_time', 'importance']

    def clean_status(self):
        status = self.cleaned_data.get('status')

        if status == "IN_PROGRESS":
            if TaskEntryModel.objects.filter(user=self.instance.user, status="IN_PROGRESS").exclude(id=self.instance.id).exists():
                raise forms.ValidationError("You can only have one task in progress at a time.")
        
        return status