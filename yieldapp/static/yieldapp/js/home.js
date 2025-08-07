// Menunggu sampai seluruh halaman HTML selesai dimuat
document.addEventListener('DOMContentLoaded', function() {
    
    // 1. Temukan semua elemen yang ingin kita animasikan
    const elementsToReveal = document.querySelectorAll('.hero-content .reveal');

    // 2. Loop melalui setiap elemen dan tampilkan satu per satu
    elementsToReveal.forEach((element, index) => {
        // Beri jeda waktu berdasarkan urutannya (index)
        // Elemen pertama muncul setelah 100ms, kedua 300ms, ketiga 500ms
        setTimeout(() => {
            element.classList.add('visible');
        }, 200 * index + 100); 
    });

});