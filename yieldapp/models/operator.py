# models/operator.py
from django.db import models
from .core import BatchInfo

class OperatorYieldData(models.Model):
    # --- I. DEFINISI FIELD (KOLOM DATABASE) ---
    batch = models.ForeignKey(BatchInfo, on_delete=models.CASCADE, related_name="yield_data")
    tanggal_proses = models.DateField(help_text="Tanggal dimulainya proses batch ini")
    
    # Field Output Proses
    formulation_output_kg = models.FloatField(null=True, blank=True, verbose_name="Output Formulasi (Kg)")
    formulation_output_pcs = models.PositiveIntegerField(null=True, blank=True, verbose_name="Output Formulasi (setara Pcs)")
    filling_output = models.PositiveIntegerField(null=True, blank=True)
    
    # Field Inspeksi yang sudah benar
    inspection_output = models.PositiveIntegerField(null=True, blank=True, verbose_name="Jumlah Lolos Inspeksi (pcs)")
    qc_sample = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name="Jumlah Sampel QC (pcs)")
    
    assembly_output = models.PositiveIntegerField(null=True, blank=True)
    blistering_output = models.PositiveIntegerField(null=True, blank=True)
    packaging_output = models.PositiveIntegerField(null=True, blank=True)
    handover_output = models.PositiveIntegerField(null=True, blank=True, verbose_name="Handover to Warehouse (pcs)")
    created_at = models.DateTimeField(auto_now_add=True)

    # --- II. LOGIKA KALKULASI (SEPERTI RUMUS OTOMATIS) ---
    
    @property
    def total_after_inspection(self):
        """Menjumlahkan hasil inspeksi dan sampel QC."""
        good_inspection = self.inspection_output or 0
        sample = self.qc_sample or 0
        return good_inspection + sample

    # A. Perhitungan Yield Akhir
    @property
    def final_yield_percentage(self):
        """Menghitung persentase yield akhir."""
        if self.handover_output is None or self.batch.product.theoritical_yield_pcs == 0:
            return 0.0
        yield_calc = (self.handover_output / self.batch.product.theoritical_yield_pcs) * 100
        return round(yield_calc, 2)

    @property
    def target_yield(self):
        """Mengambil target yield dari master product."""
        return self.batch.product.target_yield_percent

    @property
    def is_achieved(self):
        """Mengecek apakah yield mencapai target."""
        return self.final_yield_percentage >= self.target_yield

    # B. Perhitungan Loss per Tahap
    @property
    def loss_filling(self):
        start = self.formulation_output_pcs or 0
        end = self.filling_output or 0
        return start - end if start > 0 and end > 0 else 0

    @property
    def loss_inspection(self):
        start = self.filling_output or 0
        end = self.total_after_inspection # Menggunakan total_after_inspection yang sudah kita buat
        return start - end if start > 0 and end > 0 else 0

    @property
    def loss_assembly(self):
        start = self.total_after_inspection
        end = self.assembly_output or 0
        return start - end if start > 0 and end > 0 else 0

    @property
    def loss_blistering(self):
        start = self.assembly_output or 0
        end = self.blistering_output or 0
        return start - end if start > 0 and end > 0 else 0
    
    @property
    def loss_packaging(self):
        start = self.blistering_output or 0
        end = self.packaging_output or 0
        return start - end if start > 0 and end > 0 else 0

    @property
    def loss_handover(self):
        start = self.packaging_output or 0
        end = self.handover_output or 0
        return start - end if start > 0 and end > 0 else 0

    # --- III. PENGATURAN MODEL ---
    def __str__(self):
        return f"Batch {self.batch} - {self.tanggal_proses}"

    class Meta:
        verbose_name = "Data Yield Operator"
        verbose_name_plural = "Data Yield Operator"
        ordering = ['-tanggal_proses', 'batch']