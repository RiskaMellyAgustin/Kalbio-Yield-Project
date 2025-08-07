# yieldapp/views.py

from django.shortcuts import render
from django.db.models import Count, Q, Avg, F, FloatField
from django.core.paginator import Paginator # <-- 1. IMPORT Paginator
from ..models import Product, OperatorYieldData, BatchInfo, Issue
import json
from datetime import datetime

def unified_dashboard(request):
    # --- 1. AMBIL DATA DASAR & PILIHAN FILTER ---
    # Gunakan order_by() agar hasil pagination konsisten
    base_query = OperatorYieldData.objects.filter(batch__status='Completed').select_related('batch', 'batch__product').order_by('-batch__start_date')
    
    available_years = base_query.dates('batch__start_date', 'year', order='DESC')
    available_products = Product.objects.filter(batches__status='Completed').distinct()
    wip_batches = BatchInfo.objects.exclude(status='Completed').select_related('product').order_by('-start_date')

    # --- 2. TERAPKAN FILTER ---
    selected_year = request.GET.get('year')
    selected_month = request.GET.get('month')
    selected_product = request.GET.get('product')
    start_date_filter = request.GET.get('start_date')
    end_date_filter = request.GET.get('end_date')

    filtered_yields = base_query
    if selected_year:
        filtered_yields = filtered_yields.filter(batch__start_date__year=selected_year)
    if selected_month:
        filtered_yields = filtered_yields.filter(batch__start_date__month=selected_month)
    if selected_product:
        filtered_yields = filtered_yields.filter(batch__product_id=selected_product)
    if start_date_filter:
        filtered_yields = filtered_yields.filter(batch__start_date__gte=start_date_filter)
    if end_date_filter:
        filtered_yields = filtered_yields.filter(batch__start_date__lte=end_date_filter)

    # --- 3. KALKULASI BERDASARKAN DATA YANG SUDAH DIFILTER ---
    # Pindahkan kalkulasi ini sebelum pagination agar tetap menghitung total dari semua data yang difilter
    total_batches = filtered_yields.count()
    achieved_count = sum(1 for yd in filtered_yields if yd.is_achieved)# Lebih efisien daripada loop Python
    filtered_batch_ids = filtered_yields.values_list('batch_id', flat=True)
    total_issues = Issue.objects.filter(batch_id__in=filtered_batch_ids).count()

    donut_data = {'labels': ['Target Tercapai', 'Tidak Tercapai'], 'data': [achieved_count, total_batches - achieved_count]}
    
    # ... (logika chart lainnya tetap sama)
    yield_per_product = (
        Product.objects.filter(batches__id__in=filtered_batch_ids)
        .annotate(avg_yield=Avg(F('batches__yield_data__handover_output') * 100.0 / F('theoritical_yield_pcs')))
        .filter(avg_yield__isnull=False).order_by('-avg_yield')
    )
    bar_data = {
        'labels': [p.name for p in yield_per_product],
        'data': [round(p.avg_yield, 2) if p.avg_yield else 0 for p in yield_per_product],
    }
    
    # --- 4. IMPLEMENTASI PAGINATION ---
    # Tentukan jumlah item per halaman, misalnya 10
    paginator = Paginator(filtered_yields, 10) 
    page_number = request.GET.get('page')
    # get_page() menangani nomor halaman yang tidak valid secara otomatis
    page_obj = paginator.get_page(page_number) 

    # --- 5. LOGIKA DETAIL PER BATCH (WATERFALL) ---
    selected_batch_id = request.GET.get('batch_detail')
    selected_batch_data_for_template = None
    waterfall_data = []

    if selected_batch_id:
        # Cukup cari dari base_query karena detail tidak terpengaruh pagination
        sbd = base_query.filter(pk=selected_batch_id).first()
        if sbd:
            selected_batch_data_for_template = sbd
            waterfall_data = [
                sbd.batch.product.theoritical_yield_pcs, -sbd.loss_filling, -sbd.loss_inspection,
                -sbd.loss_assembly, -sbd.loss_blistering, -sbd.loss_packaging, -sbd.loss_handover
            ]

    # --- DAFTAR BULAN UNTUK FILTER ---
    months = [(i, datetime(2000, i, 1).strftime('%B')) for i in range(1, 13)]

    context = {
        'wip_batches': wip_batches,
        'available_years': available_years,
        'available_months': months,
        'available_products': available_products,
        'selected_year': selected_year,
        'selected_month': selected_month,
        'selected_product': selected_product,
        'start_date_filter': start_date_filter,
        'end_date_filter': end_date_filter,
        
        # Ganti 'filtered_yield_data' dengan 'page_obj' untuk data tabel
        'page_obj': page_obj,  # <-- 4. KIRIM PAGE OBJECT
        
        # Kalkulasi global tetap menggunakan data sebelum pagination
        'total_completed_batches': total_batches,
        'achieved_rate': round((achieved_count / total_batches) * 100, 1) if total_batches > 0 else 0,
        'total_issues': total_issues,
        
        'donut_chart_data': json.dumps(donut_data),
        'bar_chart_data': json.dumps(bar_data),
        
        'selected_batch_data': selected_batch_data_for_template,
        'waterfall_labels': json.dumps(['Theoretical', 'Loss Filling', 'Loss Inspection', 'Loss Assembly', 'Blistering', 'Packaging', 'Handover', 'Final Yield']),
        'waterfall_data': json.dumps(waterfall_data),
    }
    
    return render(request, 'yieldapp/dashboard/unified_dashboard.html', context)