from django import forms
from ..models import issueActionPlan
from ..models.issueActionPlan import Issue


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description"]
        widgets = {
            "title": forms.TextInput(attrs={"required": True}),
            "description": forms.Textarea(attrs={"rows": 4, "required": True}),
        }
