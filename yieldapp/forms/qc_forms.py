from django import forms
from ..models import BatchInfo

class QCPCTForm(forms.ModelForm):
    class Meta:
        model = BatchInfo
        # Tentukan field mana saja yang akan muncul di form
        fields = [
            'qc_sample_received_date',
            'qc_report_handed_over_date',
        ]
        # Gunakan widget DateInput agar muncul kalender di browser
        widgets = {
            'qc_sample_received_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'qc_report_handed_over_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }