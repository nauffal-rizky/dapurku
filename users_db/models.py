from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Sum

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

class UserAddress(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
  street = models.CharField(max_length=255)
  house_no = models.CharField(max_length=50, blank=True)
  rtrw = models.CharField(max_length=20, blank=True)
  kelurahan = models.CharField(max_length=100)
  kecamatan = models.CharField(max_length=100)
  city = models.CharField(max_length=100)
  province = models.CharField(max_length=100)
  postal_code = models.CharField(max_length=10)
  is_default = models.BooleanField(default=False)  # For selecting a primary address

  def __str__(self):
    return f"{self.street}, {self.city}, {self.province}"

  class Meta:
    unique_together = ('user', 'is_default')  # Ensure only one default per user (optional)

class Product(models.Model):
  CATEGORY_CHOICES = [
    ('makanan', 'Makanan'),
    ('minuman', 'Minuman'),
    ('camilan', 'Camilan'),
    ('lainnya', 'Lainnya'),
  ]

  name = models.CharField(max_length=50)
  description = models.TextField(blank=False)
  price = models.DecimalField(max_digits=10, decimal_places=2)
  stock = models.PositiveIntegerField(default=1, editable=True)
  image = models.ImageField(upload_to='product_images/', blank=False)
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
    """Recalculate stock based on variants."""
    total_stock = self.variants.aggregate(total=models.Sum('stock'))['total'] or 0
    self.stock = total_stock
    self.save(update_fields=['stock'])

class Order(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  address = models.ForeignKey('UserAddress', on_delete=models.SET_NULL, null=True, blank=True)  # NEW: Link to selected address
  total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  created_at = models.DateTimeField(auto_now_add=True)
  status = models.CharField(max_length=20, default="Pending")
  midtrans_transaction_id = models.CharField(max_length=100, blank=True, null=True)  # NEW: For tracking MidTrans txn

  def __str__(self):
    return f"Order #{self.id} by {self.user.username}"

class OrderItem(models.Model):
  order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
  product = models.ForeignKey(Product, on_delete=models.CASCADE)
  quantity = models.PositiveIntegerField(default=1)
  price = models.DecimalField(max_digits=10, decimal_places=2)

  def get_total(self):
    return self.price * self.quantity

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
  quantity = models.PositiveIntegerField(default=1)

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)

  class Meta:
    unique_together = ("user", "product")  # 1 user ga bisa duplikat produk yg sama + variant

  def __str__(self):
    return f"{self.user.username} - {self.product.name} ({self.quantity})"

  @property
  def total_price(self):
    base_price = self.product.price
    return base_price * self.quantity
