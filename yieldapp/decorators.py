from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied

def group_required(*group_names):
    """
    Decorator untuk view yang memeriksa apakah pengguna adalah anggota
    dari setidaknya salah satu grup yang diberikan.
    """
    def check_perms(user):
        # Superuser selalu diizinkan
        if user.is_superuser:
            return True
        # Cek apakah pengguna sudah login dan ada di salah satu grup yang diizinkan
        if user.is_authenticated and user.groups.filter(name__in=group_names).exists():
            return True
        # Jika tidak, tolak akses
        raise PermissionDenied
        
    return user_passes_test(check_perms, login_url='/login/')

# Kita buat decorator spesifik untuk setiap peran agar mudah digunakan
operator_required = group_required('Operator')
mstd_required = group_required('MSTD', 'Manajemen') # MSTD & Manajemen bisa akses halaman MSTD
manajemen_required = group_required('Manajemen')
qc_required = group_required('QC', 'Manajemen') # QC & Manajemen bisa akses halaman QC