from django.shortcuts import render, get_object_or_404
from ..models.core import BatchInfo
from ..models.operator import OperatorYieldData

# View untuk halaman utama dashboard operator
def operator_dashboard(request):
    # Ambil semua batch yang statusnya BUKAN 'Selesai'
    wip_batches = BatchInfo.objects.exclude(status='Completed').order_by('-start_date')

    context = {
        'wip_batches': wip_batches,
        'selected_batch': None, # Awalnya belum ada batch yang dipilih
    }
    return render(request, 'yieldapp/dashboard/dashboard_operator/operator_dashboard.html', context)

# View saat operator mengklik salah satu batch di sidebar
def batch_process_view(request, batch_pk):
    wip_batches = BatchInfo.objects.exclude(status='Completed').order_by('-start_date')
    selected_batch = get_object_or_404(BatchInfo, pk=batch_pk)
    
    # Ambil data yield yang terkait dengan batch ini
    yield_data = OperatorYieldData.objects.filter(batch=selected_batch).first()

    context = {
        'wip_batches': wip_batches,
        'selected_batch': selected_batch,
        'yield_data': yield_data, # Kirim data yield ke template
    }
    return render(request, 'yieldapp/dashboard/dashboard_operator/operator_dashboard.html', context)