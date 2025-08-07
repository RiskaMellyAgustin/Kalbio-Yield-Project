# yieldapp/urls.py

from django.urls import path
from . import views
# Impor semua view yang kita butuhkan dengan nama yang konsisten
from .views import landing, mstd, operator, dashboard, dashboard_operator, issue, quality, central, auth, uploads, report_view

urlpatterns = [
    # HALAMAN UTAMA
    path('', landing.home_page, name='home'),

    # --- URLS UNTUK MSTD ---
     
    path('mstd/dashboard/', mstd.mstd_hub, name='mstd_dashboard'), # URL untuk hub MSTD
    path('mstd/products/', mstd.product_list, name='product_list'),
    path('mstd/products/', mstd.product_list, name='product_list'),
    path('mstd/products/edit/<int:pk>/', mstd.product_edit, name='product_edit'),
    path('mstd/issues/', mstd.issue_list, name='issue_list'), 
    # Nama 'update_action' agar cocok dengan template teman Anda
    path('mstd/issues/<int:issue_pk>/update/', mstd.update_action_plan, name='update_action'),

    # --- URLS UNTUK OPERATOR ---
    # Dashboard utama operator
    path('operator/dashboard/', dashboard_operator.operator_dashboard, name='operator_dashboard'),
    path('operator/dashboard/batch/<int:batch_pk>/', dashboard_operator.batch_process_view, name='batch_process_view'),
    # Halaman input data proses
    path('input/filling/', operator.input_filling, name='input_filling'),
    path('input/inspection/<int:pk>/', operator.input_inspection, name='input_inspection'),
    path('input/assembly/<int:pk>/', operator.input_assembly, name='input_assembly'),
    path('input/blistering/<int:pk>/', operator.input_blistering, name='input_blistering'),
    path('input/packaging/<int:pk>/', operator.input_packaging, name='input_packaging'),
    path('input/handover/<int:pk>/', operator.input_handover, name='input_handover'),
    path('input/success/<int:pk>/', operator.handover_success, name='handover_success'),

    # --- URLS UNTUK FITUR ISU (DARI SISI OPERATOR) ---
    # Nama 'report_issue' agar lebih jelas, sesuai view yang kita buat
    path('batch/<int:batch_pk>/issue/', issue.report_issue, name='report_issue'),
    
    # --- URLS UNTUK QUALITY (QC/QA) ---
    path('quality/qc/dashboard/', quality.qc_dashboard, name='qc_dashboard'),
    path('quality/qc/update/<int:batch_pk>/', quality.qc_update_pct, name='qc_update_pct'),

    # --- URL UNTUK DASHBOARD MANAJEMEN ---
    path('dashboard/', dashboard.unified_dashboard, name='dashboard'), 
    path('notifications/', mstd.notification_list, name='notification_list'),
    
     # --- URL BARU UNTUK OTENTIKASI ---
    path('login/', auth.login_view, name='login'),
    path('logout/', auth.logout_view, name='logout'),
    path('redirect/', auth.redirect_hub, name='redirect_hub'),\
    # --------------------------------
    path('upload/yield/', uploads.upload_yield_csv, name='upload_yield'),
    path('upload/products/', uploads.upload_product_csv, name='upload_product'), 
    path('upload/review/', uploads.review_staged_data, name='upload_review'), 
    path('upload/process/', uploads.process_staged_data, name='process_staged_data'),
    
     path('report/print/', report_view.print_report_view, name='print_report'),
    
    
    
    # path('report/print/', views.print_report_view, name='print_report'),
    
    # path('api/batch-detail/<int:pk>/', dashboard.batch_detail_api, name='batch_detail_api'),
    
    # --- URL BARU UNTUK DASBOR TERPUSAT ---
    path('central-dashboard/', central.central_dashboard, name='central_dashboard'),
]