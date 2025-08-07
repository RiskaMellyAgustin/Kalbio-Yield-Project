document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('formModal');
    const modalContent = document.getElementById('modalContent');
    const closeModalButton = document.querySelector('.close-button');
    const clickableElements = document.querySelectorAll('[data-url]');

    // --- FUNGSI YANG DIPERBAIKI ---
    function openModal() { 
        // Tambahkan kelas .is-visible untuk menampilkan & menengahkan
        modal.classList.add('is-visible'); 
    }

    function closeModal() { 
        // Hapus kelas .is-visible untuk menyembunyikan
        modal.classList.remove('is-visible');
        modalContent.innerHTML = ''; 
    }
    // ----------------------------

    if (closeModalButton) {
        closeModalButton.addEventListener('click', closeModal);
    }
    window.addEventListener('click', function(event) {
        if (event.target == modal) { closeModal(); }
    });

    clickableElements.forEach(element => {
        if (element.dataset.url) {
            element.addEventListener('click', function(event) {
                event.preventDefault();
                const formUrl = this.dataset.url;
                
                modalContent.innerHTML = '<p style="text-align:center; color: #9CA3AF;">Memuat form...</p>';
                openModal();
                fetch(formUrl)
                    .then(response => response.text())
                    .then(html => { modalContent.innerHTML = html; })
                    .catch(error => {
                        console.error('Gagal memuat form:', error);
                        modalContent.innerHTML = '<p>Gagal memuat form. Silakan coba lagi.</p>';
                    });
            });
        }
    });
});