from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from ..models import BatchInfo
from ..forms.qc_forms import QCPCTForm

def qc_dashboard(request):
    """
    Menampilkan daftar batch yang relevan untuk diupdate oleh tim QC.
    Contoh: Batch yang sudah selesai produksi tapi belum di-release oleh QA.
    """
    batches_for_qc = BatchInfo.objects.filter(status='Completed', qa_release_date__isnull=True).order_by('-start_date')
    
    context = {
        'batches': batches_for_qc
    }
    return render(request, 'yieldapp/quality/qc_dashboard.html', context)


def qc_update_pct(request, batch_pk):
    """
    Menampilkan form untuk mengupdate tanggal PCT untuk satu batch
    dan menyimpan perubahannya.
    """
    batch = get_object_or_404(BatchInfo, pk=batch_pk)
    if request.method == 'POST':
        form = QCPCTForm(request.POST, instance=batch)
        if form.is_valid():
            form.save()
            messages.success(request, f"Data PCT untuk batch {batch.batch_number} berhasil disimpan.")
            return redirect('qc_dashboard')
    else:
        form = QCPCTForm(instance=batch)
    
    context = {
        'form': form, 
        'batch': batch
    }
    return render(request, 'yieldapp/quality/qc_update_form.html', context)