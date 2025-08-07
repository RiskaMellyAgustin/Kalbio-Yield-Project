# yieldapp/forms/mstd_forms.py

from django import forms
from ..models import Product, Issue
# yieldapp/forms/mstd_forms.py

# Import Product model

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # Masukkan kembali 'theoritical_yield_pcs' dan 'target_yield_percent' di sini
        fields = ["product_code", "name", "theoritical_yield_pcs", "target_yield_percent"] 
        widgets = {
            "product_code": forms.TextInput(attrs={"class": "form-control"}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            # Tambahkan widget untuk field-field ini agar tampilannya konsisten
            "theoritical_yield_pcs": forms.NumberInput(attrs={"class": "form-control"}),
            "target_yield_percent": forms.NumberInput(attrs={"class": "form-control"}),
        }

# Kelas form lainnya (ActionForm, dll.) tetap sama di file ini.

class ActionForm(forms.ModelForm):
    is_resolved = forms.BooleanField(required=False, label="Tandai sebagai selesai")

    class Meta:
        model = Issue
        fields = ["action_taken", "is_resolved"]
        widgets = {
            "action_taken": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "is_resolved": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }