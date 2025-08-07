# yieldapp/models/staging.py
from django.db import models
from django.contrib.auth.models import User

class StagingYieldData(models.Model):
    # Sesuaikan field-field ini dengan kolom CSV yang Anda harapkan
    # Ini adalah model untuk menampung data sementara dari upload CSV sebelum diproses ke tabel utama

    batch_number = models.CharField(max_length=255, null=True, blank=True)
    product_name = models.CharField(max_length=255, null=True, blank=True)
    product_code = models.CharField(max_length=255, null=True, blank=True) # Tambahkan ini untuk Product Code
    start_date = models.CharField(max_length=255, null=True, blank=True) # Biarkan sebagai CharField dulu untuk fleksibilitas tanggal

    # Pastikan field ini ditambahkan jika Anda akan menggunakannya untuk proses staging dan validasi
    theoritical_yield_pcs = models.CharField(max_length=255, null=True, blank=True)
    target_yield_percent = models.CharField(max_length=255, null=True, blank=True)

    formulation_kg = models.CharField(max_length=255, null=True, blank=True)
    formulation_pcs = models.CharField(max_length=255, null=True, blank=True)
    filling_pcs = models.CharField(max_length=255, null=True, blank=True)
    inspection_pcs = models.CharField(max_length=255, null=True, blank=True)
    qc_sample_pcs = models.CharField(max_length=255, null=True, blank=True)
    assembly_pcs = models.CharField(max_length=255, null=True, blank=True)
    blistering_pcs = models.CharField(max_length=255, null=True, blank=True)
    packaging_pcs = models.CharField(max_length=255, null=True, blank=True)
    handover_pcs = models.CharField(max_length=255, null=True, blank=True)
    issue_description = models.TextField(null=True, blank=True)

    # Status untuk proses staging
    status_choices = [
        ('PENDING', 'Pending Proses'),
        ('SUCCESS', 'Berhasil Diproses'),
        ('ERROR', 'Gagal Diproses'),
    ]
    status = models.CharField(max_length=10, choices=status_choices, default='PENDING')
    error_message = models.TextField(null=True, blank=True)

    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) # Untuk melacak kapan data staging terakhir diupdate

    def __str__(self):
        return f"Staging: {self.batch_number or 'N/A'} - {self.product_name or 'N/A'} ({self.status})"