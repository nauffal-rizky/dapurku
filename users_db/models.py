from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('suspended', 'Suspended'),
    ]

    username = models.CharField(max_length=30, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    user_status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    description = models.TextField(blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_umkm = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

class Product(models.Model):
  CATEGORY_CHOICES = [
    ('makanan', 'Makanan'),
    ('minuman', 'Minuman'),
    ('camilan', 'Camilan'),
    ('lainnya', 'Lainnya'),
  ]

  name = models.CharField(max_length=100)
  description = models.TextField(blank=True)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField(default=0, editable=False)
  image = models.ImageField(upload_to='product_images/', blank=True, null=True)
  category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
  is_available = models.BooleanField(default=True)

  sold = models.PositiveIntegerField(default=0)
  rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  umkm_user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def update_stock(self):
    """Hitung ulang stock berdasarkan semua varian."""
    total_stock = self.variants.aggregate(total=models.Sum('stock'))['total'] or 0
    self.stock = total_stock
    self.save(update_fields=['stock'])

class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants"
    )
    name = models.CharField(max_length=100)
    additional_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.product.name} - {self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_stock()  # update otomatis setelah save

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.update_stock()  # update otomatis setelah delete


class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"{self.product.name} x {self.quantity} by {self.user.username}"

class Cart(models.Model):
  user = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="cart_items"
  )
  product = models.ForeignKey(
    Product,
    on_delete=models.CASCADE,
    related_name="cart_items"
  )
  variant = models.ForeignKey(
    ProductVariant,
    on_delete=models.SET_NULL,
    null=True, blank=True,
    related_name="cart_items"
  )
  quantity = models.PositiveIntegerField(default=1)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ("user", "product", "variant")  # 1 user ga bisa duplikat produk yg sama + variant

  def __str__(self):
    return f"{self.user.username} - {self.product.name} ({self.quantity})"

  @property
  def total_price(self):
    base_price = self.product.price
    if self.variant:
      base_price += self.variant.additional_price
    return base_price * self.quantity
