// // Menunggu sampai seluruh halaman HTML selesai dimuat
// yieldapp/static/yieldapp/js/unified_dashboard.js
document.addEventListener('DOMContentLoaded', function() {
    const dataElement = document.getElementById('dashboard-data');
    if (!dataElement) return;

    const allData = JSON.parse(dataElement.textContent);

    // Render Chart Umum
    const donutCtx = document.getElementById('donutChart');
    if (donutCtx && allData.donutData) {
        new Chart(donutCtx, {
            type: 'doughnut', data: { labels: allData.donutData.labels, datasets: [{ data: allData.donutData.data, backgroundColor: ['#73946B', '#E74C3C'] }] }
        });
    }

    const barCtx = document.getElementById('barChart');
    if (barCtx && allData.barData) {
        new Chart(barCtx, {
            type: 'bar', data: { labels: allData.barData.labels, datasets: [{ label: 'Rata-rata Yield (%)', data: allData.barData.data, backgroundColor: '#537D5D' }] },
            options: { indexAxis: 'y', plugins: { legend: { display: false } } }
        });
    }

    // Render Chart Detail jika ada datanya
    if (allData.selectedBatchData) {
        const batchData = allData.selectedBatchData;
        const waterfallCtx = document.getElementById('waterfallChart');
        if (waterfallCtx) {
            new Chart(waterfallCtx, {
                type: 'bar', data: { labels: batchData.waterfallLabels, datasets: [{ label: 'Yield Flow (pcs)', data: batchData.waterfallData, backgroundColor: ['#537D5D', '#E74C3C', '#E74C3C', '#E74C3C', '#E74C3C', '#E74C3C', '#E74C3C'], waterfall: { calculating: true } }] },
                options: { plugins: { legend: { display: false } } }
            });
        }
        const barDetailCtx = document.getElementById('barDetailChart');
        if (barDetailCtx) {
            new Chart(barDetailCtx, {
                type: 'bar', data: { labels: ['Yield Performance'], datasets: [{ label: 'Actual Yield (%)', data: [batchData.finalYield], backgroundColor: '#9EBC8A' }, { label: 'Target Yield (%)', data: [batchData.targetYield], backgroundColor: '#D2D0A0' }] },
                options: { scales: { y: { beginAtZero: true, max: 110 } } }
            });
        }
    }
});
// document.addEventListener('DOMContentLoaded', function() {

//     // Ambil data JSON yang sudah disiapkan dari Django di dalam tag <script>
//     const chartDataElement = document.getElementById('dashboard-data');
//     if (!chartDataElement) return; // Hentikan jika data tidak ada

//     const data = JSON.parse(chartDataElement.textContent);

//     // --- 1. Render Grafik Umum (selalu ada) ---
    
//     // Donut Chart
//     const donutCtx = document.getElementById('donutChart');
//     if (donutCtx && data.donutData) {
//         new Chart(donutCtx, {
//             type: 'doughnut',
//             data: {
//                 labels: data.donutData.labels,
//                 datasets: [{
//                     data: data.donutData.data,
//                     backgroundColor: ['#73946B', '#E74C3C'], // Warna hijau & merah
//                     hoverOffset: 4
//                 }]
//             },
//             options: {
//                 responsive: true,
//                 maintainAspectRatio: false
//             }
//         });
//     }

//     // Bar Chart
//     const barCtx = document.getElementById('barChart');
//     if (barCtx && data.barData) {
//         new Chart(barCtx, {
//             type: 'bar',
//             data: {
//                 labels: data.barData.labels,
//                 datasets: [{
//                     label: 'Rata-rata Yield (%)',
//                     data: data.barData.data,
//                     backgroundColor: '#537D5D' // Warna hijau gelap
//                 }]
//             },
//             options: {
//                 indexAxis: 'y',
//                 scales: { x: { beginAtZero: true, max: 100 } },
//                 plugins: { legend: { display: false } },
//                 responsive: true,
//                 maintainAspectRatio: false
//             }
//         });
//     }

//     // --- 2. Render Grafik Detail (hanya jika batch dipilih) ---
    
//     if (data.selectedBatchData) {
//         // Waterfall Chart
//         const waterfallCtx = document.getElementById('waterfallChart');
//         if (waterfallCtx) {
//             new Chart(waterfallCtx, {
//                 type: 'bar',
//                 data: {
//                     labels: data.selectedBatchData.waterfallLabels,
//                     datasets: [{
//                         label: 'Yield Flow (pcs)',
//                         data: data.selectedBatchData.waterfallData,
//                         backgroundColor: ['#537D5D', '#E74C3C', '#E74C3C', '#E74C3C', '#E74C3C', '#E74C3C', '#E74C3C'],
//                         waterfall: { calculating: true }
//                     }]
//                 },
//                 options: {
//                     plugins: { legend: { display: false } },
//                     responsive: true,
//                     maintainAspectRatio: false
//                 }
//             });
//         }

//         // Bar Chart Detail
//         const barDetailCtx = document.getElementById('barDetailChart');
//         if (barDetailCtx) {
//             new Chart(barDetailCtx, {
//                 type: 'bar',
//                 data: {
//                     labels: ['Yield Performance'],
//                     datasets: [
//                         { label: 'Actual Yield (%)', data: [data.selectedBatchData.finalYield], backgroundColor: '#9EBC8A' },
//                         { label: 'Target Yield (%)', data: [data.selectedBatchData.targetYield], backgroundColor: '#D2D0A0' }
//                     ]
//                 },
//                 options: {
//                     scales: { y: { beginAtZero: true, max: 110 } },
//                     responsive: true,
//                     maintainAspectRatio: false
//                 }
//             });
//         }
//     }
// });