from django.db import models
from .master import Product
import datetime

class BatchInfo(models.Model):
    PROCESS_STAGES = [
        ("Formulation", "Formulasi"),
        ("Filling", "Filling"),
        ("Inspection", "Inspeksi"),
        ("Assembly", "Assembly"),
        ("Blistering", "Blistering"),
        ("Packaging", "Packaging"),
        ("Handover", "Handover"),
        ("Completed", "Selesai"),
    ]

    batch_number = models.CharField(max_length=255, unique=True)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name="batches")
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(
        max_length=50,
        choices=PROCESS_STAGES,
        default="Formulation",
        verbose_name="Status Proses",
    )
    
    qc_sample_received_date = models.DateField(null=True, blank=True, verbose_name="Tanggal Sampel Diterima QC")
    qc_report_handed_over_date = models.DateField(null=True, blank=True, verbose_name="Tanggal Laporan QAR Diserahkan ke QA")
    qa_release_date = models.DateField(null=True, blank=True, verbose_name="Tanggal Batch Dirilis oleh QA")

    # # --- TAMBAHKAN DUA FIELD INI ---
    # theoritical_yield_pcs = models.PositiveIntegerField(verbose_name="Theoretical Yield (pcs)")
    # target_yield_percent = models.FloatField(verbose_name="Target Yield (%)")
    # # -------------------------------

    def __str__(self):
        return f"{self.batch_number} - {self.product.name}"

    class Meta:
        verbose_name = "Informasi Batch"
        verbose_name_plural = "Informasi Batch"

class Notification(models.Model):
    message = models.TextField(help_text="Isi pesan notifikasi.")
    timestamp = models.DateTimeField(auto_now_add=True)
    link = models.URLField(
        blank=True, null=True, help_text="Link opsional ke halaman detail."
    )

    def __str__(self):
        return self.message

    class Meta:
        ordering = ["-timestamp"]