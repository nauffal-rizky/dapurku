import logging
import json
import xendit
from xendit import invoice
import logging

# Set up logging for debugging
logger = logging.getLogger(__name__)

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# umkm/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# ✅ Import your dashboard helper functions
from .utils import get_umkm_dashboard_data, get_customer_dashboard_data

from django.forms import inlineformset_factory

from django.db import transaction
from django.db.models import Sum
from users_db.models import CustomUser, Product, Order, OrderItem, Cart, UserAddress
from users_db.forms import RegisterForm, ProductForm, ProfileUpdateForm


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
  "add_address",
  "update_address",
  "order_list",
]

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

def frontPage(request):
  page = "front"

  fourLatestProducts = Product.objects.filter().order_by('-created_at')[:3]

  contents = {'page': page, 'plain_page': page in plain_pages, 'fourLatestProducts': fourLatestProducts} 
  return render(request, "./pages/frontpage.html", contents) 

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
  umkmProducts = Product.objects.filter(umkm_user_id=product.umkm_user_id).exclude(pk=pk)[:4]
  otherProducts = Product.objects.exclude(umkm_user_id=product.umkm_user_id)
  
  contents = {
    'page': page,
    'plain_page': page in plain_pages,
    "product": product,
    'umkmProducts': umkmProducts,
    'otherProducts': otherProducts
  }
  
  return render(request, './pages/product-detail.html', contents)

@login_required(login_url = 'login')
@transaction.atomic
def manage_product(request, pk=None):
  user = request.user
  page = "edit_product" if pk else "add_product"

  product = get_object_or_404(Product, pk=pk, umkm_user_id=user) if pk else None

  form = ProductForm(request.POST or None, request.FILES or None, instance=product)

  if request.method == "POST":
    if form.is_valid():
      product = form.save(commit=False)
      product.umkm_user_id = user
      product.save()

      messages.success(request, f"Produk {'diperbarui' if pk else 'berhasil ditambahkan'}!")
      return redirect("profile")

    else:
      messages.error(request, "Terdapat kesalahan pada form. Periksa kembali.")
      print("FORM ERRORS:", form.errors)

  context = {
    "page": page,
    "plain_page": page in plain_pages,
    "form": form,
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
  products = Cart.objects.filter(user=request.user).order_by('-created_at')

  context = {
    "page": "order",
    "plain_page": "order" in plain_pages,
    "user": request.user,
    "products": products,
  }
  return render(request, "./pages/order.html", context)

@login_required
def order_list(request):
  page = "order_list"
  orders = Cart.objects.filter(user=request.user)

  context = {
    'page': page,
    'plain_page': page in plain_pages,
    'orders': orders,
  }
  return render(request, './pages/order_list.html', context)

@login_required(login_url = 'login')
def cartPage(request):
  page = "cart" 
  cart_items = Cart.objects.filter(user=request.user)
  subtotal = sum(item.total_price for item in cart_items)

  context = {
    'page': page,
    'plain_page': page in plain_pages,
    "cart_items": cart_items,
    "subtotal": subtotal,
    "addresses": request.user.addresses.all(),
  }
  return render(request, "./pages/cartpage.html", context)

@login_required(login_url="login")
def add_to_cart(request, product_id):
  product = get_object_or_404(Product, pk=product_id)
  quantity = int(request.POST.get("quantity", 1))


  cart_item, created = Cart.objects.get_or_create(
    user=request.user,
    product=product,
    defaults={"quantity": quantity},
  )

  if not created:
    cart_item.quantity += quantity
    cart_item.save()

  messages.success(request, f"{product.name} berhasil ditambahkan ke keranjang!")
  return redirect(request.META.get('HTTP_REFERER', 'products'))

@login_required
def update_cart_item(request, item_id):
  if request.method == 'POST':
    data = json.loads(request.body)
    quantity = data.get('quantity')
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.quantity = quantity
    item.save()
    return JsonResponse({'success': True})
  return JsonResponse({'success': False})

@login_required(login_url="login")
def delete_cart_item(request, cart_item_id):
  cart_item = get_object_or_404(Cart, pk=cart_item_id, user=request.user)
  
  try:
    product_name = cart_item.product.name  # Store name for message
    cart_item.delete()
    messages.success(request, f"{product_name} berhasil dihapus dari keranjang!")
  except Cart.DoesNotExist:  # This shouldn't happen with get_object_or_404, but kept for safety
    messages.error(request, "Item tidak ditemukan di keranjang.")

  return redirect(request.META.get('HTTP_REFERER', 'cart'))

def contactPage(request):
  page = "contact"
  
  if request.method == 'POST':
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    
    if not all([name, email, message]):
      messages.error(request, "Semua field harus diisi.")
      return redirect('contact')
    
    subject = f"Pesan Kontak dari {name}"
    body = f"Nama: {name}\nEmail: {email}\nPesan:\n{message}"
    recipient = 'contact@dapurku.store'
    
    try:
      send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, [recipient])
      messages.success(request, "Pesan Anda telah dikirim! Kami akan segera menghubungi Anda.")
    except Exception as e:
      messages.error(request, f"Gagal mengirim pesan: {str(e)}")
    
    return redirect('contact')
  
  contents = {'page': page, 'plain_page': page in plain_pages}
  return render(request, './pages/contact.html', contents)

@login_required
def manage_address(request, address_id=None):
  # Determine if this is an add or update operation
  if address_id:
    address = get_object_or_404(UserAddress, id=address_id, user=request.user)  # Ensure ownership
    page = "update_address"
  else:
    address = None
    page = "add_address"
  
  if request.method == 'POST':
    # Extract form data
    street = request.POST.get('street')
    house_no = request.POST.get('house_no')
    rtrw = request.POST.get('rtrw')
    kelurahan = request.POST.get('kelurahan')
    kecamatan = request.POST.get('kecamatan')
    city = request.POST.get('city')
    province = request.POST.get('province')
    postal_code = request.POST.get('postal_code')
    
    # Validate: Ensure all fields are filled
    if not all([street, house_no, rtrw, kelurahan, kecamatan, city, province, postal_code]):
        messages.error(request, "Semua field harus diisi.")
        # Re-render the form with existing data to avoid losing input
        contents = {
            'page': page,
            'address': address,
            'plain_page': page in plain_pages,  # Assuming plain_pages is defined elsewhere
            'action_url': f'/address/manage/{address.id}/' if address else '/address/manage/',
            'form_data': request.POST,  # Pass POST data back to pre-fill on error
        }
        return render(request, 'pages/manage-address.html', contents)
    
    if address:
        # Update existing address
        address.street = street
        address.house_no = house_no
        address.rtrw = rtrw
        address.kelurahan = kelurahan
        address.kecamatan = kecamatan
        address.city = city
        address.province = province
        address.postal_code = postal_code
        address.save()
        messages.success(request, "Alamat berhasil diperbarui!")
    else:
        # Create new address
        UserAddress.objects.create(
            user=request.user,
            street=street,
            house_no=house_no,
            rtrw=rtrw,
            kelurahan=kelurahan,
            kecamatan=kecamatan,
            city=city,
            province=province,
            postal_code=postal_code
        )
        messages.success(request, "Alamat berhasil ditambahkan!")
    
    return redirect('cart')
  
  # For GET requests, render the form
  contents = {
      'page': page,
      'address': address,
      'plain_page': page in plain_pages,  # Assuming plain_pages is defined elsewhere
      'action_url': f'/address/manage/{address.id}/' if address else '/address/manage/',
      'form_data': None,  # No pre-fill on initial load
  }
  return render(request, 'pages/manage-address.html', contents)

  if request.method == 'POST':
    try:
      data = json.loads(request.body)
      invoice_id = data['id']
      status = data['status']  # 'PAID', 'EXPIRED', etc.

      order = Order.objects.get(xendit_invoice_id=invoice_id)
      if status == 'PAID':
        order.status = 'paid'  # Update your Order model
        # Add logic: e.g., reduce stock, send confirmation
      elif status == 'EXPIRED':
        order.status = 'failed'
      order.save()
      return JsonResponse({'status': 'ok'})
    except Exception as e:
      logger.error(f"Webhook error: {e}")
      return JsonResponse({'error': 'Invalid webhook'}, status=400)
  return JsonResponse({'error': 'Method not allowed'}, status=405)