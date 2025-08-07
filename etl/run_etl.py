import os
import sys
import django

# Tambahkan folder backend ke path agar bisa import project Django
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

# Set DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "kalbio_dashboard.settings")
django.setup()

# Setelah setup, baru import modul ETL
from etl.etl_process import run_etl

# Jalankan ETL
run_etl()
