# yieldapp/admin.py

from django.contrib import admin
# Impor semua model yang ingin kita lihat di admin panel
from .models import Product, BatchInfo, OperatorYieldData, Issue, Notification

# Daftarkan setiap model
admin.site.register(Product)
admin.site.register(BatchInfo)
admin.site.register(OperatorYieldData)
admin.site.register(Issue)          # <-- INI YANG DITAMBAHKAN
admin.site.register(Notification)   # <-- INI JUGA