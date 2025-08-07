# yieldapp/forms/operator_forms.py
from django import forms
from ..models.operator import OperatorYieldData
from ..models.master import Product
from ..models.core import BatchInfo
from ..models.issueActionPlan import Issue

# ... (import dan form lainnya biarkan sama) ...


class CreateBatchForm(forms.Form):
    batch_number = forms.CharField(
        label="Nomor Batch",
        max_length=50,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Contoh: BATCH-001"}
        ),
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        label="Pilih Produk",
        empty_label="--- Pilih Produk ---",
        widget=forms.Select(attrs={"class": "form-control"}),
    )
    tanggal_proses = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date", "class": "form-control"}),
        label="Tanggal Proses",
    )

    # --- TAMBAHKAN INPUT INI ---
    formulation_output_kg = forms.FloatField(
        label="Hasil Formulasi Aktual (Kg)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    formulation_output_pcs = forms.IntegerField(
        label="Hasil Formulasi (setara Pcs)",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    # ---------------------------

    filling_output = forms.IntegerField(
        label="Hasil Filling Aktual (Pcs)",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )

    # --- INI LOGIKANYA ---
    def clean_batch_number(self):
        """Metode untuk memvalidasi keunikan nomor batch."""
        # 1. Ambil data nomor batch dari input operator
        batch_number = self.cleaned_data.get("batch_number")

        # 2. Cek apakah nomor batch ini sudah ada di database
        if BatchInfo.objects.filter(batch_number=batch_number).exists():
            # 3. Jika ADA, hentikan proses dan kirim pesan error ke form
            raise forms.ValidationError(
                "Nomor Batch ini sudah digunakan. Harap masukkan nomor yang berbeda."
            )

        # 4. Jika TIDAK ADA, kembalikan data agar bisa diproses lebih lanjut
        return batch_number


class InspectionForm(forms.ModelForm):
    class Meta:
        model = OperatorYieldData
        # --- PASTIKAN BAGIAN INI BENAR ---
        # Tampilkan kedua field ini di form
        fields = ['inspection_output', 'qc_sample']
        # ---------------------------------
        widgets = {
            'inspection_output': forms.NumberInput(attrs={'class': 'form-control'}),
            'qc_sample': forms.NumberInput(attrs={'class': 'form-control'})
        }


class AssemblyForm(forms.ModelForm):
    class Meta:
        model = OperatorYieldData
        fields = ["assembly_output"]


class BlisteringForm(forms.ModelForm):
    class Meta:
        model = OperatorYieldData
        fields = ["blistering_output"]


class PackagingForm(forms.ModelForm):
    class Meta:
        model = OperatorYieldData
        fields = ["packaging_output"]


class HandoverForm(forms.ModelForm):
    class Meta:
        model = OperatorYieldData
        fields = ["handover_output"]


class IssueForm(forms.ModelForm):
    class Meta:
        model = Issue
        fields = ["title", "description"]
