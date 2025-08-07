# yieldapp/utils/notif.py

from django.urls import reverse
from ..models.core import Notification


def create_completion_notification(batch):
    """
    Membuat satu notifikasi publik (pengumuman) di database.
    """
    try:
        message = f"Proses untuk batch {batch.batch_number} telah selesai."
        # Pastikan Anda memiliki URL dengan nama 'batch_process_view'
        link_to_batch = reverse("batch_process_view", kwargs={"batch_pk": batch.pk})

        Notification.objects.create(message=message, link=link_to_batch)
        print(f"Pengumuman untuk batch {batch.batch_number} berhasil dibuat.")
    except Exception as e:
        print(f"ERROR: Gagal membuat pengumuman: {e}")
