# # yieldapp/views/operator.py
# # yieldapp/views/operator.py
# from django.shortcuts import render, get_object_or_404, redirect
# from ..forms.operator_forms import *  # <--- UBAH MENJADI SEPERTI INI
# from ..models.operator import OperatorYieldData
# from django.db import transaction
# from ..models.operator import OperatorYieldData
# from ..models.core import BatchInfo
# from ..forms.operator_forms import IssueForm
# from ..models.issueActionPlan import Issue
# from django.contrib import messages
# from ..models.issueActionPlan import Issue
# from ..models.core import BatchInfo
# yieldapp/views/operator.py

from django.shortcuts import render, get_object_or_404, redirect
from django.db import transaction
from ..utils.notif import create_completion_notification
from django.utils import timezone 

# Import Form yang dibutuhkan
from ..forms.operator_forms import (
    CreateBatchForm,
    InspectionForm,
    AssemblyForm,
    BlisteringForm,
    PackagingForm,
    HandoverForm
)

# Import Model yang dibutuhkan
from ..models.operator import OperatorYieldData
from ..models.core import BatchInfo

# Import fungsi notifikasi
from ..utils.notif import create_completion_notification

@transaction.atomic
def input_filling(request):
    if request.method == "POST":
        form = CreateBatchForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            new_batch = BatchInfo.objects.create(
                batch_number=cleaned_data["batch_number"],
                product=cleaned_data["product"],
                start_date=cleaned_data["tanggal_proses"],
            )
            OperatorYieldData.objects.create(
                batch=new_batch,
                tanggal_proses=cleaned_data["tanggal_proses"],
                formulation_output_kg=cleaned_data["formulation_output_kg"],
                formulation_output_pcs=cleaned_data["formulation_output_pcs"],
                filling_output=cleaned_data["filling_output"],
            )
            return redirect("operator_dashboard")
    else:
        form = CreateBatchForm()

    return render(
        request,
        "yieldapp/operator/input_form.html",
        {"form": form, "proses": "Langkah 1: Formulasi & Filling (Mulai Batch Baru)"},
    )

def input_inspection(request, pk):
    # 1. Ambil data yield yang mau di-update berdasarkan ID
    data = get_object_or_404(OperatorYieldData, pk=pk)
    
    # 2. Jika operator menekan tombol "Simpan" (method POST)
    if request.method == "POST":
        # Masukkan data dari request ke dalam form
        form = InspectionForm(request.POST, instance=data)
        if form.is_valid():
            form.save() # Simpan data baru (inspection_output dan qc_sample)
            data.batch.status = "Inspection" # Update status batch
            data.batch.save()
            # Arahkan kembali ke dashboard operator untuk melihat progres
            return redirect("batch_process_view", batch_pk=data.batch.pk)
    else:
        # 3. Jika halaman baru dibuka (method GET), tampilkan form yang sudah ada datanya
        form = InspectionForm(instance=data)

    # 4. Render template 'form_partial.html' untuk ditampilkan di dalam modal
    return render(
        request,
        "yieldapp/operator/partials/form_partial.html",
        {"form": form, "proses": f"Update Hasil Inspeksi (Batch: {data.batch.batch_number})"},
    )
# def input_inspection(request, pk):
#     data = get_object_or_404(OperatorYieldData, pk=pk)
#     if request.method == "POST":
#         form = InspectionForm(request.POST, instance=data)
#         if form.is_valid():
#             form.save()
#             data.batch.status = "Inspection"
#             data.batch.save()
#             return redirect("batch_process_view", batch_pk=data.batch.pk)
#     else:
#         form = InspectionForm(instance=data)

#     return render(
#         request,
#         "yieldapp/operator/partials/form_partial.html",
#         {"form": form, "proses": "Input Hasil Inspeksi"},
#     )


def input_assembly(request, pk):
    data = get_object_or_404(OperatorYieldData, pk=pk)
    if request.method == "POST":
        form = AssemblyForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            data.batch.status = "Assembly"
            data.batch.save()
            return redirect("batch_process_view", batch_pk=data.batch.pk)
    else:
        form = AssemblyForm(instance=data)
    return render(
        request,
        "yieldapp/operator/partials/form_partial.html",
        {"form": form, "proses": "Input Hasil Assembly"},
    )


def input_blistering(request, pk):
    data = get_object_or_404(OperatorYieldData, pk=pk)
    if request.method == "POST":
        form = BlisteringForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            data.batch.status = "Blistering"
            data.batch.save()
            return redirect("batch_process_view", batch_pk=data.batch.pk)
    else:
        form = BlisteringForm(instance=data)
    return render(
        request,
        "yieldapp/operator/partials/form_partial.html",
        {"form": form, "proses": "Input Hasil Blistering"},
    )


def input_packaging(request, pk):
    data = get_object_or_404(OperatorYieldData, pk=pk)
    if request.method == "POST":
        form = PackagingForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            data.batch.status = "Packaging"
            data.batch.save()
            return redirect("batch_process_view", batch_pk=data.batch.pk)
    else:
        form = PackagingForm(instance=data)
    return render(
        request,
        "yieldapp/operator/partials/form_partial.html",
        {"form": form, "proses": "Input Hasil Packaging"},
    )

def input_handover(request, pk):
    data = get_object_or_404(OperatorYieldData, pk=pk)
    if request.method == "POST":
        form = HandoverForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            data.batch.status = "Completed"
            
            # --- TAMBAHKAN BARIS INI ---
            # Set tanggal selesai produksi menjadi tanggal hari ini
            data.batch.end_date = timezone.now().date()
            # ---------------------------

            data.batch.save() # Simpan perubahan status dan end_date
            
            # Panggil fungsi notifikasi setelah batch selesai
            create_completion_notification(data.batch)
            
            return redirect("handover_success", pk=data.pk)
    else:
        form = HandoverForm(instance=data)
        
    return render(
        request,
        "yieldapp/operator/partials/form_partial.html",
        {"form": form, "proses": f'Input Hasil Handover (Batch: {data.batch.batch_number})'},
    )
    
def handover_success(request, pk):
    """
    Menampilkan halaman konfirmasi setelah semua proses input selesai.
    """
    # Ambil data yang baru saja diselesaikan untuk ditampilkan di halaman sukses
    data = get_object_or_404(OperatorYieldData, pk=pk)
    context = {
        'data': data
    }
    return render(request, "yieldapp/operator/handover_success.html", context)

# def input_handover(request, pk):
#     data = get_object_or_404(OperatorYieldData, pk=pk)
#     if request.method == "POST":
#         form = HandoverForm(request.POST, instance=data)
#         if form.is_valid():
#             form.save()
#             data.batch.status = "Completed"
#             data.batch.save()
#             # Panggil fungsi notifikasi setelah batch selesai
#             create_completion_notification(data.batch)
#             return redirect("operator_dashboard")
#     else:
#         form = HandoverForm(instance=data)
#     return render(
#         request,
#         "yieldapp/operator/partials/form_partial.html",
#         {"form": form, "proses": "Input Hasil Handover"},
#     )
    
# def input_handover(request, pk):
#     data = get_object_or_404(OperatorYieldData, pk=pk)
#     if request.method == 'POST':
#         form = HandoverForm(request.POST, instance=data)
#         if form.is_valid():
#             form.save()
#             data.batch.status = 'Completed'
#             data.batch.save()
            
#             # --- PANGGIL FUNGSI NOTIFIKASI DI SINI ---
#             create_completion_notification(data.batch)
#             # ----------------------------------------

#             return redirect('operator_dashboard')
#     else:
#         form = HandoverForm(instance=data)
    
#     return render(request, 'yieldapp/operator/partials/form_partial.html', {
#         'form': form, 
#         'proses': f'Input Hasil Handover (Batch: {data.batch.batch_number})'
#     })
