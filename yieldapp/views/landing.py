from django.shortcuts import render

def home_page(request):
    """
    View ini hanya bertugas untuk menampilkan halaman utama (landing page).
    """
    context = {} # Tidak perlu mengirim data apa pun untuk halaman ini
    return render(request, 'yieldapp/home.html', context)