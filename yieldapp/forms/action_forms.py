# yieldapp/forms/action_forms.py
from django import forms
from ..models.issueActionPlan import Issue


class ActionForm(forms.ModelForm):
    is_resolved = forms.BooleanField(required=False, label="Tandai sebagai selesai")

    class Meta:
        model = Issue
        fields = ["action_taken", "is_resolved"]
        widgets = {
            "action_taken": forms.Textarea(attrs={"rows": 4}),
        }
