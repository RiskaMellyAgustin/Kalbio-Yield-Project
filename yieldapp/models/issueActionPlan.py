# models/issueActionPlan.py
from django.db import models
from .core import BatchInfo

class Issue(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_resolved = models.BooleanField(default=False)
    action_taken = models.TextField(blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # --- HANYA ADA SATU DEFINISI 'batch' ---
    batch = models.ForeignKey(
        BatchInfo, 
        on_delete=models.CASCADE, 
        related_name='issues'
    )
    # ------------------------------------

    def __str__(self):
        return self.title