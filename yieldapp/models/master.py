from django.db import models


class Product(models.Model):
    # Kunci Unik Baru
    product_code = models.CharField(
        max_length=50, unique=True, 
        verbose_name="Kode Produk Unik"
    )
    name = models.CharField(
        max_length=100, 
        verbose_name="Nama Produk"
        # unique=True dihapus dari sini
    )
    theoritical_yield_pcs = models.PositiveIntegerField(
        verbose_name="Theoretical Yield (pcs)"
    )
    target_yield_percent = models.FloatField(
        verbose_name="Target Yield (%)"
    )

    def __str__(self):
        return f"{self.name} ({self.product_code})"


# class Product(models.Model):
#     name = models.CharField(max_length=100, unique=True, verbose_name="Nama Produk")
#     theoritical_yield_pcs = models.PositiveIntegerField(
#         verbose_name="Theoretical Yield (pcs)",
#         help_text="Jumlah unit produk yang seharusnya dihasilkan secara teori.",
#     )
#     target_yield_percent = models.FloatField(
#         verbose_name="Target Yield (%)",
#         help_text="Target persentase yield yang diharapkan untuk produk ini.",
#     )

#     # PASTIKAN BAGIAN INI BENAR
#     def __str__(self):
#         return self.name

#     class Meta:
#         verbose_name = "Master Produk"
#         verbose_name_plural = "Master Produk"
