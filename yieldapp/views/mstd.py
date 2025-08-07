# yieldapp/views/mstd.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Impor model yang dibutuhkan
from ..models import Product, Issue, Notification
# Impor form dari file spesifiknya (INI PERBAIKANNYA)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..decorators import mstd_required
from ..models import Product, Issue, Notification
from ..forms.mstd_forms import ProductForm
from ..forms.action_forms import ActionForm


# -- VIEW BARU UNTUK HALAMAN UTAMA MSTD --
@login_required
@mstd_required
def mstd_hub(request):
    """
    Menampilkan halaman utama (hub) untuk MSTD dengan pilihan menu.
    """
    return render(request, "yieldapp/dashboard/mstd_dashboard.html")


# == Manajemen Data Master Produk ==
@login_required
@mstd_required
def product_list(request):
    products = Product.objects.all().order_by("name")
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f"Produk '{form.cleaned_data['name']}' berhasil ditambahkan.")
            return redirect("product_list")
    else:
        form = ProductForm()
    return render(request, "yieldapp/mstd/product_list.html", {"form": form, "products": products})

def product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, f"Produk '{product.name}' berhasil diperbarui.")
            return redirect("product_list")
    else:
        form = ProductForm(instance=product)
    return render(request, "yieldapp/mstd/product_edit.html", {"form": form})


@login_required
@mstd_required
# == Manajemen Isu & Tindak Lanjut (Peran MSTD/Manajemen) ==
def issue_list(request):
    issues = Issue.objects.select_related('batch', 'batch__product').all().order_by("-created_at")
    return render(request, "yieldapp/mstd/issue_list.html", {"issues": issues})

@login_required
@mstd_required
def update_action_plan(request, issue_pk):
    issue = get_object_or_404(Issue, pk=issue_pk)
    if request.method == "POST":
        form = ActionForm(request.POST, instance=issue)
        if form.is_valid():
            form.save()
            messages.success(request, "Rencana tindak lanjut berhasil disimpan!")
            return redirect("issue_list")
    else:
        form = ActionForm(instance=issue)
    return render(request, "yieldapp/mstd/action_form.html", {"form": form, "issue": issue})


@login_required
@mstd_required
# == Halaman Notifikasi ==
def notification_list(request):
    notifications = Notification.objects.all()
    return render(request, "yieldapp/mstd/notification_list.html", {"notifications": notifications})