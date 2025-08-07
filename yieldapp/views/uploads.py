# yieldapp/views/uploads.py

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import transaction
from django.contrib.auth.decorators import login_required
from ..decorators import mstd_required
from django.db.utils import IntegrityError 

from ..forms.upload_forms import CSVUploadForm, ProductCSVUploadForm 

from ..models import Product, BatchInfo, OperatorYieldData, Issue
from ..models.staging import StagingYieldData


# Fungsi pembantu untuk membersihkan nilai numerik dari string
def clean_numeric(value, to_type=int, allow_negative=False):
    """
    Membersihkan dan mengonversi nilai string menjadi numerik (int atau float).
    Menangani NaN, string kosong, N/A, None, dan #VALUE! dari Excel.
    Mengganti koma dengan titik untuk desimal.
    """
    if pd.isna(value) or str(value).strip().lower() in ['nan', '', 'n/a', 'none', '#value!']:
        return None
    
    cleaned_value = str(value).strip().replace(',', '.') 
    
    if to_type == int:
        cleaned_value = ''.join(c for c in cleaned_value if c.isdigit() or (c == '-' and cleaned_value.index(c) == 0))
    else: # float
        cleaned_value = ''.join(c for c in cleaned_value if c.isdigit() or c == '.' or (c == '-' and cleaned_value.index(c) == 0))

    if not cleaned_value or cleaned_value == '.' or cleaned_value == '-': 
        return None
    
    try:
        num = float(cleaned_value)
        if not allow_negative:
            num = abs(num) 
        return to_type(num)
    except ValueError:
        return None 

# --- Fungsi Upload CSV Data Yield (untuk migrasi data historis) ---
@login_required
@mstd_required
def upload_yield_csv(request):
    """
    Mengunggah file CSV yang berisi data yield historis ke area staging (StagingYieldData).
    Data akan ditinjau sebelum diproses ke tabel utama.
    """
    if request.method == 'POST':
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File harus berformat .csv.')
                return redirect('upload_yield')

            try:
                # Membersihkan data staging yang diupload oleh user ini sebelumnya
                StagingYieldData.objects.filter(uploaded_by=request.user).delete()

                df = None
                try:
                    csv_file.seek(0)
                    # Coba baca dengan delimiter ;
                    df_test = pd.read_csv(csv_file, sep=';', nrows=1)
                    if len(df_test.columns) > 1:
                        csv_file.seek(0)
                        df = pd.read_csv(csv_file, sep=';')
                    else:
                        raise ValueError("Delimiter ; tidak efektif.")
                except Exception:
                    csv_file.seek(0)
                    df = pd.read_csv(csv_file, sep=',')
                
                if df is None or df.empty:
                    messages.warning(request, "File CSV kosong atau tidak dapat dibaca.")
                    return redirect('upload_yield')

                df.dropna(how='all', inplace=True)
                if df.empty:
                    messages.warning(request, "File CSV kosong setelah menghapus baris kosong.")
                    return redirect('upload_yield')

                df = df.astype(str)
                
                uploaded_rows_count = 0
                total_errors_in_csv = [] 

                # KAMUS HEADER CSV DARI cleaned_yield_dataset.csv
                # PASTIKAN KOLOM INI ADA DI CSV DAN MENGGUNAKAN NAMA YANG SAMA PERSIS (case-sensitive)
                csv_header_to_staging_field = {
                    'Product Code': 'product_code', 
                    'Product': 'product_name',
                    'Batch Number': 'batch_number', 
                    'Date (Formulation)': 'start_date',
                    'Theoritical Yield (pcs)': 'theoritical_yield_pcs', 
                    'Target Yield': 'target_yield_percent',              
                    'Output Formulation (to Filling) (Kg)': 'formulation_kg',
                    'Output Formulation (to Filling) (Pcs)': 'formulation_pcs',
                    'Output Filling (to Inspection) (pcs)': 'filling_pcs',
                    'Good Inspection + QC Sample(to Assembly) (pcs)': 'inspection_pcs',
                    'QC Sample': 'qc_sample_pcs', 
                    'Good Assembly (pcs)': 'assembly_pcs',
                    'Good Blistering (pcs)': 'blistering_pcs',
                    'Good Packaging (pcs)': 'packaging_pcs',
                    'Handover to Warehouse (pcs)': 'handover_pcs',
                    'Issue/Problem': 'issue_description',
                }

                # Memvalidasi keberadaan kolom penting di CSV yang diunggah
                required_csv_cols_for_upload = [
                    'Product Code', 'Product', 'Batch Number', 'Date (Formulation)', 
                    'Theoritical Yield (pcs)', 'Target Yield', 
                    'Output Formulation (to Filling) (Pcs)', 'Handover to Warehouse (pcs)'
                ]
                missing_cols_in_uploaded_csv = [col for col in required_csv_cols_for_upload if col not in df.columns]
                if missing_cols_in_uploaded_csv:
                    messages.error(request, f"File CSV Data Yield tidak memiliki kolom wajib: {', '.join(missing_cols_in_uploaded_csv)}. Harap periksa template.")
                    return redirect('upload_yield')

                for index, row in df.iterrows():
                    try:
                        StagingYieldData.objects.create(
                            uploaded_by=request.user,
                            batch_number=row.get('Batch Number', ''),
                            product_name=row.get('Product', ''),
                            product_code=row.get('Product Code', ''),
                            start_date=row.get('Date (Formulation)', ''),
                            theoritical_yield_pcs=row.get('Theoritical Yield (pcs)', ''),
                            target_yield_percent=row.get('Target Yield', ''),
                            formulation_kg=row.get('Output Formulation (to Filling) (Kg)', ''),
                            formulation_pcs=row.get('Output Formulation (to Filling) (Pcs)', ''),
                            filling_pcs=row.get('Output Filling (to Inspection) (pcs)', ''),
                            inspection_pcs=row.get('Good Inspection + QC Sample(to Assembly) (pcs)', ''),
                            qc_sample_pcs=row.get('QC Sample', ''),
                            assembly_pcs=row.get('Good Assembly (pcs)', ''),
                            blistering_pcs=row.get('Good Blistering (pcs)', ''),
                            packaging_pcs=row.get('Good Packaging (pcs)', ''),
                            handover_pcs=row.get('Handover to Warehouse (pcs)', ''),
                            issue_description=row.get('Issue/Problem', ''),
                            status='PENDING' 
                        )
                        uploaded_rows_count += 1
                    except KeyError as e:
                        total_errors_in_csv.append(f"Baris {index + 2}: Kolom '{e.args[0]}' tidak ditemukan di CSV. Mohon periksa header CSV Anda.")
                    except Exception as e:
                        total_errors_in_csv.append(f"Baris {index + 2}: Gagal menyimpan ke staging. Pesan: {e}")

                if uploaded_rows_count > 0:
                    messages.success(request, f"Berhasil mengunggah {uploaded_rows_count} baris data ke area staging. Silakan tinjau dan proses data.")
                if total_errors_in_csv:
                    messages.error(request, f"Gagal mengunggah {len(total_errors_in_csv)} baris ke staging. Beberapa detail: {'; '.join(total_errors_in_csv[:min(5, len(total_errors_in_csv))])}{'...' if len(total_errors_in_csv) > 5 else ''}")
                
                return redirect('upload_review') 
            
            except Exception as e:
                messages.error(request, f"Gagal membaca atau memproses file CSV. Pastikan format, header kolom, dan separatornya benar. Error: {e}")
                return redirect('upload_yield')
    else:
        form = CSVUploadForm()
    return render(request, 'yieldapp/uploads/upload_page.html', {'form': form})


# --- Fungsi Upload CSV Master Produk (TIDAK BERUBAH) ---
@login_required
@mstd_required
@transaction.atomic
def upload_product_csv(request):
    """
    Mengunggah dan memproses file CSV yang berisi data master produk.
    Data akan mengupdate atau membuat entri baru di model Product.
    """
    if request.method == 'POST':
        form = ProductCSVUploadForm(request.POST, request.FILES) 
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File harus berformat .csv.')
                return redirect('upload_product')

            try:
                df = None
                try:
                    csv_file.seek(0)
                    df_test = pd.read_csv(csv_file, sep=';', nrows=1)
                    if len(df_test.columns) > 1:
                        csv_file.seek(0)
                        df = pd.read_csv(csv_file, sep=';')
                    else:
                        raise ValueError("Delimiter ; tidak efektif.")
                except Exception:
                    csv_file.seek(0)
                    df = pd.read_csv(csv_file, sep=',')
                
                if df is None or df.empty:
                    messages.warning(request, "File CSV kosong atau tidak dapat dibaca.")
                    return redirect('upload_product')

                df.dropna(how='all', inplace=True)
                if df.empty:
                    messages.warning(request, "File CSV kosong setelah menghapus baris kosong.")
                    return redirect('upload_product')

                df = df.astype(str)

                column_mapping_product = {
                    'Product Code': 'product_code', 
                    'Product Name': 'name',        
                    'Theoritical Yield (pcs)': 'theoritical_yield_pcs', 
                    'Target Yield': 'target_yield_percent',             
                }
                
                required_cols_product_csv = ['Product Code', 'Product Name', 'Theoritical Yield (pcs)', 'Target Yield'] 
                missing_cols_product = [col for col in required_cols_product_csv if col not in df.columns]
                if missing_cols_product:
                    messages.error(request, f"File CSV Master Produk tidak memiliki kolom wajib: {', '.join(missing_cols_product)}. Harap periksa template.")
                    return redirect('upload_product')

                df.rename(columns=column_mapping_product, inplace=True)

                success_count = 0
                errors = []
                for index, row in df.iterrows():
                    try:
                        product_code = row.get('product_code', '').strip()
                        product_name = row.get('name', '').strip()
                        theoritical_yield_pcs_val = clean_numeric(row.get('theoritical_yield_pcs'), int)
                        target_yield_percent_val = clean_numeric(row.get('target_yield_percent'), float)

                        if not product_code:
                            raise ValueError("Kode Produk kosong di baris ini.")
                        if not product_name:
                            raise ValueError("Nama Produk kosong di baris ini.")
                        if theoritical_yield_pcs_val is None:
                            raise ValueError("Theoretical Yield (pcs) kosong atau tidak valid di baris ini.")
                        if target_yield_percent_val is None:
                            raise ValueError("Target Yield (%) kosong atau tidak valid di baris ini.")
                        
                        product, created = Product.objects.update_or_create(
                            product_code=product_code,
                            defaults={
                                'name': product_name,
                                'theoritical_yield_pcs': theoritical_yield_pcs_val, 
                                'target_yield_percent': target_yield_percent_val 
                            }
                        )
                        success_count += 1
                    except IntegrityError as e:
                        errors.append(f"Baris {index + 2} (Kode: '{row.get('product_code', 'N/A')}'): Kode produk sudah ada. Pesan: {e}")
                    except ValueError as e:
                        errors.append(f"Baris {index + 2} (Kode: '{row.get('product_code', 'N/A')}'): Data tidak valid. Pesan: {e}")
                    except Exception as e:
                        errors.append(f"Baris {index + 2} (Kode: '{row.get('product_code', 'N/A')}'): Gagal memproses. Pesan: {e}")
                    
                messages.success(request, f'{success_count} data produk berhasil diimpor atau diperbarui.')
                if errors:
                    messages.error(request, f"Gagal mengimpor {len(errors)} baris produk. Beberapa detail: {'; '.join(errors[:min(5, len(errors))])}{'...' if len(errors) > 5 else ''}")
                
                return redirect('product_list')

            except Exception as e:
                messages.error(request, f"Gagal membaca atau memproses file CSV. Pastikan format, header kolom, dan separatornya benar. Error: {e}")
                return redirect('upload_product')
    else:
        form = ProductCSVUploadForm()
    return render(request, 'yieldapp/uploads/upload_product_page.html', {'form': form})


# --- Fungsi Staging Data (Review & Process) ---
@login_required
@mstd_required
def review_staged_data(request):
    """
    Menampilkan data yang baru diunggah ke area staging sebelum diproses.
    """
    staged_data = StagingYieldData.objects.filter(uploaded_by=request.user).order_by('created_at')
    context = {
        'staged_data': staged_data,
        'error_count': staged_data.filter(status='ERROR').count(),
        'success_count': staged_data.filter(status='SUCCESS').count(),
        'pending_count': staged_data.filter(status='PENDING').count()
    }
    return render(request, 'yieldapp/uploads/review_page.html', context)


@login_required
@mstd_required
def process_staged_data(request):
    """
    Memproses data dari area staging ke model utama (BatchInfo, OperatorYieldData, Issue).
    """
    if request.method == 'POST':
        staged_items = StagingYieldData.objects.filter(uploaded_by=request.user, status='PENDING')
        
        processed_count = 0
        total_errors = []

        for item in staged_items:
            try:
                with transaction.atomic():
                    product_name_cleaned = (item.product_name or '').strip()
                    product_code = (item.product_code or '').strip() 

                    if not product_name_cleaned: 
                        raise ValueError("Nama produk kosong di data staging.")
                    
                    if not product_code:
                            raise ValueError("Kode produk kosong di data staging. Tidak bisa memproses tanpa Product Code.") 

                    try:
                        product = Product.objects.get(product_code__iexact=product_code)
                    except Product.DoesNotExist:
                        raise ValueError(f"Produk '{product_name_cleaned}' dengan kode '{product_code}' tidak ditemukan di data master. Harap tambahkan terlebih dahulu.")

                    batch_number_cleaned = (item.batch_number or '').split('+')[0].strip()
                    if not batch_number_cleaned: 
                        raise ValueError("Nomor batch kosong di data staging.")
                    
                    if len(batch_number_cleaned) > 50: 
                        raise ValueError(f"Batch number '{batch_number_cleaned[:50]}...' terlalu panjang.")
                    
                    if BatchInfo.objects.filter(batch_number=batch_number_cleaned).exists():
                        raise ValueError(f"Batch '{batch_number_cleaned}' sudah ada di database utama.")
                    
                    # --- START PERBAIKAN PADA BAGIAN TANGGAL ---
                    raw_start_date_str = (item.start_date or '').strip() # Ambil string tanggal mentah dari staging

                    # Hapus suffix '.0' jika ada (terjadi jika CSV dibaca sebagai angka dan dikonversi ke string)
                    # Pastikan hanya menghapus .0 jika sisanya adalah angka
                    if raw_start_date_str.endswith('.0') and raw_start_date_str[:-2].replace('/', '').replace('-', '').isdigit():
                        raw_start_date_str = raw_start_date_str[:-2]

                    if not raw_start_date_str:
                        raise ValueError("Tanggal mulai kosong di data staging.")

                    start_date_obj = None
                    # Daftar format tanggal yang mungkin ada di CSV, coba dari yang paling spesifik
                    date_formats_to_try = [
                        '%m/%d/%Y',   # e.g., 06/24/2024
                        '%d/%m/%Y',   # e.g., 24/06/2024
                        '%m-%d-%Y',   # e.g., 06-24-2024
                        '%d-%m-%Y',   # e.g., 24-06-2024
                        '%Y/%m/%d',   # e.g., 2024/06/24
                        '%Y-%m-%d',   # e.g., 2024-06-24
                        '%m/%#d/%Y',  # e.g., 6/24/2024 (single digit month)
                        '%#m/%d/%Y',  # e.g., 6/24/2024 (single digit day)
                        '%#m/%#d/%Y', # e.g., 6/4/2024 (single digit month and day)
                        '%m%d%Y',     # e.g., 06242024 (no delimiters)
                        '%#m%#d%Y',   # e.g., 6242024 (no delimiters, single digit month/day)
                    ]

                    for fmt in date_formats_to_try:
                        try:
                            # Gunakan format yang eksplisit dan errors='raise' untuk kontrol yang lebih baik
                            start_date_obj = pd.to_datetime(raw_start_date_str, format=fmt, errors='raise').date()
                            break # Berhasil parsing, keluar dari loop
                        except ValueError:
                            continue # Coba format berikutnya

                    if start_date_obj is None:
                        # Jika semua format eksplisit gagal, coba inferensi otomatis Pandas
                        try:
                            start_date_obj = pd.to_datetime(raw_start_date_str, errors='raise', dayfirst=True).date()
                        except ValueError:
                            try:
                                start_date_obj = pd.to_datetime(raw_start_date_str, errors='raise').date()
                            except ValueError:
                                raise ValueError(f"Format tanggal '{raw_start_date_str}' di staging tidak valid setelah mencoba beberapa format.")
                    # --- END PERBAIKAN PADA BAGIAN TANGGAL ---

                    theoritical_yield_pcs_from_staging = clean_numeric(item.theoritical_yield_pcs, int)
                    target_yield_percent_from_staging = clean_numeric(item.target_yield_percent, float)

                    if theoritical_yield_pcs_from_staging is None:
                        raise ValueError("Theoretical Yield (pcs) kosong atau tidak valid di data staging.")
                    if target_yield_percent_from_staging is None:
                        raise ValueError("Target Yield (%) kosong atau tidak valid di data staging.")

                    product.theoritical_yield_pcs = theoritical_yield_pcs_from_staging
                    product.target_yield_percent = target_yield_percent_from_staging
                    product.save()

                    batch = BatchInfo.objects.create(
                        batch_number=batch_number_cleaned, 
                        product=product, 
                        start_date=start_date_obj,
                        end_date=start_date_obj, 
                        status='Completed' 
                    )
                    
                    OperatorYieldData.objects.create(
                        batch=batch, 
                        tanggal_proses=start_date_obj,
                        formulation_output_kg=clean_numeric(item.formulation_kg, float),
                        formulation_output_pcs=clean_numeric(item.formulation_pcs, int),
                        filling_output=clean_numeric(item.filling_pcs, int),
                        inspection_output=clean_numeric(item.inspection_pcs, int),
                        qc_sample=clean_numeric(item.qc_sample_pcs, int),
                        assembly_output=clean_numeric(item.assembly_pcs, int),
                        blistering_output=clean_numeric(item.blistering_pcs, int),
                        packaging_output=clean_numeric(item.packaging_pcs, int),
                        handover_output=clean_numeric(item.handover_pcs, int)
                    )
                    
                    issue_desc = item.issue_description
                    if pd.notna(issue_desc) and str(issue_desc).strip().lower() not in ['nan', 'n/a', '']:
                        Issue.objects.create(batch=batch, title=f"Isu dari CSV Staging Batch {batch.batch_number}", description=issue_desc)
                    
                    item.status = 'SUCCESS'
                    item.error_message = None
                    processed_count += 1

            except IntegrityError as e:
                item.status = 'ERROR'
                item.error_message = f"Duplikasi data atau kunci unik melanggar: {e}"
                total_errors.append(f"Baris Batch '{item.batch_number}': {item.error_message}")
            except ValueError as e:
                item.status = 'ERROR'
                item.error_message = f"Data tidak valid: {e}"
                total_errors.append(f"Baris Batch '{item.batch_number}': {item.error_message}")
            except Exception as e:
                item.status = 'ERROR'
                item.error_message = f"Gagal memproses: {e}"
                total_errors.append(f"Baris Batch '{item.batch_number}': {item.error_message}")
            finally:
                item.save()

        messages.info(request, f'Proses validasi dan impor selesai. Berhasil memproses {processed_count} baris.')
        if total_errors:
            unique_errors = list(set(total_errors)) # Ambil pesan error yang unik
            display_errors = '; '.join(unique_errors[:min(5, len(unique_errors))])
            if len(unique_errors) > 5:
                display_errors += '...'
            messages.error(request, f"Gagal memproses {len(total_errors)} baris. Beberapa detail: {display_errors}")
                
        return redirect('upload_review')