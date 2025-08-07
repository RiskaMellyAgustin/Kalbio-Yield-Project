# yieldapp/views/issue.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import BatchInfo, Issue
from ..forms.issue_forms import IssueForm

# View ini akan dipanggil oleh tombol "Laporkan/Edit Isu" dari Dashboard Operator
def report_issue(request, batch_pk):
    """
    Menangani pembuatan dan pengeditan isu untuk sebuah batch spesifik.
    """
    batch = get_object_or_404(BatchInfo, pk=batch_pk)
    
    # Coba cari apakah sudah ada isu yang terdaftar untuk batch ini
    try:
        existing_issue = Issue.objects.get(batch=batch)
    except Issue.DoesNotExist:
        existing_issue = None

    if request.method == "POST":
        # Jika sudah ada isu, form akan mengeditnya. Jika tidak, akan membuat baru.
        form = IssueForm(request.POST, instance=existing_issue)
        if form.is_valid():
            # Jangan langsung simpan ke database
            issue = form.save(commit=False)
            # Set relasi batch secara manual
            issue.batch = batch
            issue.save()

            # Beri pesan sukses
            if existing_issue:
                messages.success(request, f"Laporan isu untuk batch {batch.batch_number} berhasil diperbarui.")
            else:
                messages.success(request, f"Laporan isu untuk batch {batch.batch_number} berhasil dibuat.")
            
            # Kembali ke halaman detail proses batch di dashboard operator
            return redirect("batch_process_view", batch_pk=batch.pk)
    else:
        # Jika halaman dibuka (GET request), tampilkan form (kosong atau terisi)
        form = IssueForm(instance=existing_issue)

    context = {
        "form": form,
        "batch": batch,
    }
    # Render template issue.html yang sudah dibuat teman Anda
    return render(request, "yieldapp/operator/issue.html", context)