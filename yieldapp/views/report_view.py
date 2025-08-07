from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta, datetime
from django.db.models import F, ExpressionWrapper, FloatField 
from ..models import OperatorYieldData, Issue, BatchInfo

def print_report_view(request):
    # --- 1. AMBIL TANGGAL DARI PARAMETER GET, ATAU GUNAKAN DEFAULT (BULAN INI) ---
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    today = timezone.now()

    if start_date_str and end_date_str and start_date_str != '' and end_date_str != '':
        # Jika parameter ada dan tidak kosong, gunakan tanggal tersebut
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        report_title = "Laporan Kinerja Produksi Kustom"
    else:
        # Jika tidak ada parameter, default ke awal hingga akhir bulan ini
        start_date = today.replace(day=1).date()
        # Untuk mencari akhir bulan, pergi ke hari pertama bulan depan lalu kurangi 1 hari
        next_month = start_date.replace(day=28) + timedelta(days=4)
        end_date = next_month - timedelta(days=next_month.day)
        report_title = "Laporan Kinerja Produksi Bulanan"

    # --- 2. QUERY DATA DENGAN ANNOTATE ---
    yield_data_in_period = OperatorYieldData.objects.filter(
        batch__end_date__range=[start_date, end_date],
        batch__status='Completed'
    ).annotate(
        calculated_yield_percentage=ExpressionWrapper(
            (F('handover_output') * 100.0) / F('batch__product__theoritical_yield_pcs'),
            output_field=FloatField()
        )
    ).select_related('batch', 'batch__product')

    issues_in_period = Issue.objects.filter(
        created_at__date__range=[start_date, end_date]
    ).select_related('batch').order_by('-created_at')

    # --- 3. HITUNG DATA UNTUK RINGKASAN ---
    total_completed = yield_data_in_period.count()
    
    achieved_count = yield_data_in_period.filter(
        calculated_yield_percentage__gte=F('batch__product__target_yield_percent')
    ).count()
    
    achieved_rate = (achieved_count / total_completed * 100) if total_completed > 0 else 0
    total_issues = issues_in_period.count()
    open_issues_count = issues_in_period.filter(is_resolved=False).count()
    
    failed_batches = yield_data_in_period.filter(
        calculated_yield_percentage__lt=F('batch__product__target_yield_percent')
    )

    # --- 4. KIRIM SEMUA DATA KE TEMPLATE ---
    context = {
        'report_title': report_title,
        'start_date': start_date,
        'end_date': end_date,
        'print_date': today,
        'total_completed': total_completed,
        'achieved_rate': round(achieved_rate, 1),
        'total_issues': total_issues,
        'open_issues_count': open_issues_count,
        'failed_batches': failed_batches,
        'recent_issues': issues_in_period,
    }
    
    return render(request, 'yieldapp/report/report_template.html', context)