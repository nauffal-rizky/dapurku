from django.shortcuts import get_object_or_404, render, redirect

from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.views.generic.list import ListView

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# umkm/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# ✅ Import your dashboard helper functions
from .utils import get_umkm_dashboard_data, get_customer_dashboard_data

from django.forms import inlineformset_factory

from django.db import transaction
from django.db.models import Sum
from users_db.models import CustomUser, Product, ProductVariant, Order, OrderItem, Cart
from users_db.forms import RegisterForm, ProductForm, ProductVariantForm, ProductVariantFormSet, ProfileUpdateForm


loginSignupPage = [
  "signup",
  "login"
]
plain_pages = [
  "signup",
  "login",
  "profile",
  "add_product",
  "edit_product",
  "delete_product",
  "cart",
  "order",
]
ProductVariantFormSet = inlineformset_factory(
  Product,
  ProductVariant,
  form=ProductVariantForm,
  extra=1,
  can_delete=True
)

def loginPage(request):
  page = "login"

  if request.user.is_authenticated:
    return redirect('/')
  else:
    if request.method == 'POST':
      username = request.POST['username']
      password = request.POST['password']
      user = authenticate(request, username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect('/')
      else:
        messages.error(request, "Username atau password salah.")

    contents = {'page': page, 'plain_page': page in plain_pages, 'loginSignupPage': page in loginSignupPage} 
    return render(request, './pages/login.html', contents)

def signupPage(request):
  page = "signup"

  if request.user.is_authenticated:
    return redirect('/')
  
  if request.method == 'POST':
    form = RegisterForm(request.POST, request.FILES)
    if form.is_valid():
      user = form.save(commit=False)
      is_umkm_flag = request.POST.get("is_umkm") == "true"
      user.is_umkm = is_umkm_flag
      user.save()
      login(request, user)
      return redirect('/')
    else:
      print("❌ FORM INVALID:", form.errors)
  else:
    form = RegisterForm()
      
  contents = {'page': page, 'form': form, 'plain_page': page in plain_pages, 'loginSignupPage': page in loginSignupPage} 
  return render(request, './pages/signup.html', contents)

@login_required(login_url = 'login')
def logoutUser(request):
  logout(request)
  return redirect('login')

@login_required(login_url = 'login')
def frontPage(request):
  page = "front"

  fourLatestProducts = Product.objects.filter().order_by('-created_at')[:4]

  contents = {'page': page, 'plain_page': page in plain_pages, 'fourLatestProducts': fourLatestProducts} 
  return render(request, "./pages/frontpage.html", contents) 

@login_required(login_url = 'login')
def aboutPage(request):
  page = "about"

  
  contents = {'page': page, 'plain_page': page in plain_pages} 
  return render(request, './pages/about.html', contents)

@login_required(login_url='login')
def profilePage(request):
  page = "profile"
  user = request.user
  products = Product.objects.filter(umkm_user_id=user)
  form = ProfileUpdateForm(request.POST, request.FILES, instance=user)

  # Handle profile update
  if request.method == 'POST':
    if form.is_valid():
      form.save()
      messages.success(request, "Profil berhasil diperbarui.")
      return redirect('profile')
  else:
    form = ProfileUpdateForm(instance=user)

  # Determine which dashboard to show
  dashboard_data = (
    get_umkm_dashboard_data(user)
    if user.is_umkm else
    get_customer_dashboard_data(user)
  )

  context = {
    'page': page,
    'plain_page': page in plain_pages,
    'user': user,
    'form': form,
    'products': products,
    'dashboard': dashboard_data
  }
  return render(request, 'pages/profile.html', context)

@login_required(login_url='login')
def umkmProfilePage(request, user_id):
  page = "umkm_profile"
  umkmProducts = Product.objects.filter(umkm_user_id=user_id)
  otherProducts = Product.objects.exclude(umkm_user_id=user_id)
  user = get_object_or_404(CustomUser, pk=user_id)

  contents = {'page': page, 'plain_page': page in plain_pages, 'user': user, 'umkmProducts': umkmProducts, 'otherProducts': otherProducts}
  return render(request, 'pages/umkmProfile.html', contents)

@login_required(login_url = 'login')
def productPage(request):
  page = "products"
  
  products = Product.objects.all()
  
  if not products:
    messages.info(request, "Tidak ada produk yang ditemukan.")

  contents = {
    'page': page,
    'plain_page': page in plain_pages,
    'products': products
  }
  return render(request, './pages/products.html', contents)

@login_required(login_url = 'login')
def productDetailPage(request, pk):
  page = "detailProduct"
  
  product = get_object_or_404(Product, pk=pk)
  soldProducts = (
        OrderItem.objects
        .filter(product=product)
        .aggregate(total=Sum('quantity'))
    )['total'] or 0
  umkmProducts = Product.objects.filter(umkm_user_id=pk)
  otherProducts = Product.objects.exclude(umkm_user_id=pk)
  
  contents = {
    'page': page,
    'plain_page': page in plain_pages,
    "product": product,
    "soldProducts": soldProducts,
    'umkmProducts': umkmProducts,
    'otherProducts': otherProducts
  }
  
  return render(request, './pages/product-detail.html', contents)

@login_required(login_url = 'login')
@transaction.atomic  # ✅ ensures data integrity
def manage_product(request, pk=None):
  """Add or edit product with optional variants."""
  user = request.user
  page = "edit_product" if pk else "add_product"

  product = get_object_or_404(Product, pk=pk, umkm_user_id=user) if pk else None

  # ✅ Initialize forms
  form = ProductForm(request.POST or None, request.FILES or None, instance=product)
  formset = ProductVariantFormSet(request.POST or None, instance=product)

  if request.method == "POST":
    if form.is_valid() and formset.is_valid():
      product = form.save(commit=False)
      product.umkm_user_id = user
      product.save()

      # ✅ Handle variants safely
      variants = formset.save(commit=False)
      has_valid_variant = False

      for variant in variants:
        # only save variants with actual data
        if variant.name or variant.additional_price or variant.stock:
          has_valid_variant = True
          variant.product = product
          variant.save()

      # ✅ Handle deletions
      for obj in formset.deleted_objects:
        obj.delete()

      # ✅ Enforce “min 1 variant” only for edits (optional)
      if pk and not has_valid_variant and not product.variants.exists():
        messages.warning(request, "Minimal 1 varian produk diperlukan.")
        return redirect("manage_product", pk=product.pk)

      messages.success(request, f"Produk {'diperbarui' if pk else 'berhasil ditambahkan'}!")
      return redirect("profile")

    else:
      messages.error(request, "Terdapat kesalah`an pada form. Periksa kembali.")
      print("FORM ERRORS:", form.errors)
      print("FORMSET ERRORS:", formset.errors)

  context = {
    "page": page,
    "plain_page": page in plain_pages,
    "form": form,
    "formset": formset,
    "product": product,
  }
  return render(request, "pages/umkm/product-form.html", context)

@login_required(login_url="login")
def delete_product(request, pk):
  page = 'delete_product'
  
  product = get_object_or_404(Product, pk=pk, umkm_user_id=request.user)
  if request.method == "POST":
    product.delete()
    return redirect("profile")

  contents = {
    "page": page,
    "plain_page": page in plain_pages,
    "product": product,
  }
  return render(request, "pages/umkm/delete-product.html", contents)

@login_required(login_url = 'login')
def orderPage(request):
  orders = Order.objects.filter(user=request.user).prefetch_related("items__product", "items__variant")

  context = {
    "page": "order",
    "plain_page": "order" in plain_pages,
    "user": request.user,
    "orders": orders,
  }
  return render(request, "./pages/order.html", context)

@login_required(login_url = 'login')
def create_order(request):
  cart_items = Cart.objects.filter(user=request.user).select_related("product", "variant")

  if not cart_items.exists():
    messages.warning(request, "Keranjang Anda kosong.")
    return redirect('cart')

  order = Order.objects.create(user=request.user, total_price=0)
  total_price = 0

  for item in cart_items:
    item_total = item.product.price * item.quantity
    OrderItem.objects.create(
      order=order,
      product=item.product,
      variant=item.variant,
      quantity=item.quantity,
      price=item.product.price
    )
    total_price += item_total

  order.total_price = total_price
  order.save()

  # Hapus keranjang setelah checkout
  cart_items.delete()

  messages.success(request, "Pesanan berhasil dibuat!")
  return redirect('order')

@login_required(login_url = 'login')
def cartPage(request):
  page = "cart" 
  cart_items = Cart.objects.filter(user=request.user).select_related("product", "variant")
  subtotal = sum(item.total_price for item in cart_items)

  context = {
    'page': page,
    'plain_page': page in plain_pages,
    "cart_items": cart_items,
    "subtotal": subtotal
  }
  return render(request, "./pages/cartpage.html", context)

@login_required(login_url="login")
def add_to_cart(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  variant_id = request.POST.get("variant_id")
  quantity = int(request.POST.get("quantity", 1))

  variant = None
  if variant_id:
    variant = get_object_or_404(ProductVariant, pk=variant_id, product=product)

  cart_item, created = Cart.objects.get_or_create(
    user=request.user,
    product=product,
    variant=variant,
    defaults={"quantity": quantity},
  )

  if not created:
    cart_item.quantity += quantity
    cart_item.save()

  messages.success(request, f"{product.name} berhasil ditambahkan ke keranjang!")
  return redirect(request.META.get('HTTP_REFERER', 'products'))

@login_required(login_url = 'login')
def contactPage(request):
  page = "contact"
  
  contents = {'page': page, 'plain_page': page in plain_pages}
  return render(request, './pages/contact.html', contents)