# yieldapp/forms/upload_forms.py
from django import forms

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Pilih file CSV")

class ProductCSVUploadForm(forms.Form):
    csv_file = forms.FileField(label="Pilih file CSV Master Produk")

# Pastikan file __init__.py ada di dalam folder 'forms'
# (Biasanya sudah ada jika itu adalah aplikasi Django)