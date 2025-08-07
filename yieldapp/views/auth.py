from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

def login_view(request):
    """Menangani proses login pengguna."""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Setelah login, arahkan ke 'redirect_hub'
            return redirect('redirect_hub')
    else:
        form = AuthenticationForm()
    return render(request, 'yieldapp/auth/login.html', {'form': form})

def logout_view(request):
    """Menangani proses logout dan mengarahkan ke halaman utama."""
    logout(request)
    return redirect('home')
# -----------------------------------

@login_required
def redirect_hub(request):
    """
    Mendeteksi peran pengguna dan mengarahkan ke dashboard yang sesuai.
    Ini adalah "stasiun pusat" setelah login.
    """
    user = request.user
    if user.is_superuser or user.groups.filter(name='Manajemen').exists():
        return redirect('dashboard') # Arahkan ke dasbor manajemen
    elif user.groups.filter(name='MSTD').exists():
        return redirect('mstd_dashboard') # Arahkan ke halaman kelola produk MSTD
    elif user.groups.filter(name='QC').exists():
        return redirect('qc_dashboard') # Arahkan ke dasbor QC
    elif user.groups.filter(name='operator').exists():
        return redirect('operator_dashboard') # Arahkan ke dasbor operator
    else:
        # Jika pengguna tidak punya grup, arahkan ke halaman utama
        return redirect('home')