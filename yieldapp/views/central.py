from django.shortcuts import render
from django.db.models import Count, Q, Avg, F, FloatField
from ..models import Product, OperatorYieldData, BatchInfo
import json

def central_dashboard(request):
    # Ambil semua data yield yang status batch-nya 'Completed'
    completed_yields = OperatorYieldData.objects.filter(batch__status='Completed')

    # 1. Data untuk Donut Chart (Target Tercapai vs Tidak)
    total_batches = completed_yields.count()
    achieved_count = 0
    if total_batches > 0:
        # Kita hitung manual karena properti @is_achieved tidak bisa di-query langsung
        achieved_batches = [yd for yd in completed_yields if yd.is_achieved]
        achieved_count = len(achieved_batches)
    
    not_achieved_count = total_batches - achieved_count

    donut_chart_data = {
        'labels': ['Target Tercapai', 'Tidak Tercapai'],
        'data': [achieved_count, not_achieved_count],
    }

    # 2. Data untuk Bar Chart (Rata-rata Yield per Produk)
    yield_per_product = (
        Product.objects.annotate(
            # Hitung rata2 yield untuk setiap produk dari batch yang sudah selesai
            avg_yield=Avg(
                'batches__yield_data__handover_output', 
                filter=Q(batches__status='Completed'),
                output_field=FloatField()
            ) * 100.0 / F('theoritical_yield_pcs')
        ).filter(avg_yield__isnull=False).order_by('-avg_yield')
    )
    
    bar_chart_data = {
        'labels': [p.name for p in yield_per_product],
        'data': [round(p.avg_yield, 2) for p in yield_per_product],
    }
    
    # 3. Data untuk kartu ringkasan
    total_issues = BatchInfo.objects.filter(status='Completed').aggregate(
        total=Count('issues')
    )['total']
    
    context = {
        'total_completed_batches': total_batches,
        'total_issues': total_issues,
        'achieved_rate': round((achieved_count / total_batches) * 100, 1) if total_batches > 0 else 0,
        'donut_chart_data': json.dumps(donut_chart_data),
        'bar_chart_data': json.dumps(bar_chart_data),
    }
    return render(request, 'yieldapp/dashboard/central_dashboard.html', context)