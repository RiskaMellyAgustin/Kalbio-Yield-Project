# yieldapp/models/merge.py

from django.db import models


class MergedYield(models.Model):
    batch_id = models.CharField(max_length=100)
    product_id = models.CharField(max_length=100)
    formulation_output_pcs = models.FloatField()
    filling_output = models.FloatField()
    inspection_output = models.FloatField()
    assembly_output = models.FloatField()
    blistering_output = models.FloatField()
    packaging_output = models.FloatField()
    handover_output = models.FloatField()
    theoritical_yield_pcs = models.FloatField()
    total_output = models.FloatField()
    yield_percent = models.FloatField()

    def __str__(self):
        return f"{self.batch_id} - {self.product_id}"
