import json
import midtransclient

from django.core.mail import send_mail
from django.template.loader import render_to_string

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import JsonResponse
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
  "order",
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

@login_required(login_url='login')
def create_order(request):
  selected_item_ids = request.POST.getlist('selected_items')
  
  if not selected_item_ids:
    messages.warning(request, "Pilih setidaknya satu produk untuk dipesan.")
    return redirect('cart')
  
  selected_address_id = request.POST.get('selected_address')
  if not selected_address_id:
    messages.warning(request, "Pilih alamat pengiriman.")
    return redirect('cart')
  
  try:
    selected_address = UserAddress.objects.get(id=selected_address_id, user=request.user)
  except UserAddress.DoesNotExist:
    messages.warning(request, "Alamat tidak ditemukan.")
    return redirect('cart')
  
  cart_items = Cart.objects.filter(user=request.user, id__in=selected_item_ids)
  
  if not cart_items.exists():
    messages.warning(request, "Produk yang dipilih tidak ditemukan di keranjang.")
    return redirect('cart')
  
  total_price = sum(item.product.price * item.quantity for item in cart_items)
  order = Order.objects.create(user=request.user, total_price=total_price, address=selected_address)
  
  for item in cart_items:
    OrderItem.objects.create(
      order=order,
      product=item.product,
      quantity=item.quantity,
      price=item.product.price
    )

  subject = f'Konfirmasi Pesanan #{order.id}'
  message = render_to_string('order_confirmation_email.html', {
      'user': request.user,
      'order': order,
      'items': order.items.all(),
      'total_price': total_price,
  })
  send_mail(subject, '', settings.DEFAULT_FROM_EMAIL, [request.user.email], html_message=message)
  
  # NEW: Integrate MidTrans payment
  snap = midtransclient.Snap(
    is_production=settings.MIDTRANS_IS_PRODUCTION,
    server_key=settings.MIDTRANS_SERVER_KEY,
    client_key=settings.MIDTRANS_CLIENT_KEY
  )
  
  # Prepare MidTrans transaction details
  transaction_details = {
    'order_id': str(order.id),  # Use your order ID
    'gross_amount': int(total_price),  # MidTrans expects integer (in IDR, assuming your prices are in IDR)
  }
  
  # Item details (optional, for MidTrans receipt)
  item_details = [
    {
      'id': str(item.product.id),
      'price': int(item.product.price),
      'quantity': item.quantity,
      'name': item.product.name,
    } for item in cart_items
  ]
  
  # Customer details
  customer_details = {
    'first_name': request.user.first_name or request.user.username,
    'last_name': request.user.last_name or '',
    'email': request.user.email,
    'phone': selected_address.phone if selected_address.phone else '',
    'billing_address': {
      'first_name': request.user.first_name or request.user.username,
      'last_name': request.user.last_name or '',
      'address': selected_address.address,
      'city': selected_address.city,
      'postal_code': selected_address.postal_code,
      'phone': selected_address.phone,
      'country_code': 'IDN'  # Adjust if needed
    },
    'shipping_address': {
      'first_name': request.user.first_name or request.user.username,
      'last_name': request.user.last_name or '',
      'address': selected_address.address,
      'city': selected_address.city,
      'postal_code': selected_address.postal_code,
      'phone': selected_address.phone,
      'country_code': 'IDN'
    }
  }
  
  # Create transaction token
  transaction = {
    'transaction_details': transaction_details,
    'item_details': item_details,
    'customer_details': customer_details,
  }
  
  try:
    transaction_token = snap.create_transaction_token(transaction)
    order.midtrans_transaction_id = transaction_details['order_id']  # Store for tracking
    order.save()
    
    # Redirect to MidTrans payment page
    return redirect(f"https://app.sandbox.midtrans.com/snap/v2/vtweb/{transaction_token['token']}")  # Use production URL if live
  except Exception as e:
    messages.error(request, f"Gagal memproses pembayaran: {str(e)}")
    order.delete()  # Rollback if payment fails
    return redirect('cart')

@login_required
def order_list(request):
  orders = Order.objects.filter(user=request.user).order_by('-created_at')
  return render(request, 'order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
  order = get_object_or_404(Order, id=order_id, user=request.user)
  return render(request, 'order_detail.html', {'order': order})

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
def add_address(request):
  if request.method == 'POST':
    # Save the address
    UserAddress.objects.create(
      user=request.user,
      street=request.POST['street'],
      house_no=request.POST.get('house_no', ''),
      rtrw=request.POST.get('rtrw', ''),
      kelurahan=request.POST['kelurahan'],
      kecamatan=request.POST['kecamatan'],
      city=request.POST['city'],
      province=request.POST['province'],
      postal_code=request.POST['postal_code'],
      is_default=not UserAddress.objects.filter(user=request.user).exists()  # Make first one default
    )
    messages.success(request, "Alamat berhasil ditambahkan!")
    return redirect('cart')
  return redirect('cart')

@login_required
def update_address(request, address_id):
  address = get_object_or_404(UserAddress, id=address_id, user=request.user)  # Ensure ownership
  if request.method == 'POST':
    # Update fields from POST data
    address.street = request.POST.get('street', address.street)
    address.house_no = request.POST.get('house_no', address.house_no)
    address.rtrw = request.POST.get('rtrw', address.rtrw)
    address.kelurahan = request.POST.get('kelurahan', address.kelurahan)
    address.kecamatan = request.POST.get('kecamatan', address.kecamatan)
    address.city = request.POST.get('city', address.city)
    address.province = request.POST.get('province', address.province)
    address.postal_code = request.POST.get('postal_code', address.postal_code)
    address.save()
    messages.success(request, "Alamat berhasil diperbarui!")
    return redirect('cart')
  # For GET, render a form (we'll handle via JS popup)
  return redirect('cart')

@login_required
def delete_address(request, address_id):
  address = get_object_or_404(UserAddress, id=address_id, user=request.user)
  if request.method == 'POST':
    address.delete()
    messages.success(request, "Alamat berhasil dihapus!")
    return redirect('cart')
  # For GET, show confirmation (we'll use JS)
  return redirect('cart')

@csrf_exempt  # MidTrans doesn't send CSRF tokens
def midtrans_webhook(request):
  if request.method == 'POST':
    data = json.loads(request.body)
    order_id = data.get('order_id')
    transaction_status = data.get('transaction_status')
    
    try:
      order = Order.objects.get(id=order_id)
      if transaction_status == 'settlement':  # Payment successful
        order.status = 'Paid'
        # Delete cart items only now
        Cart.objects.filter(user=order.user, product__in=[item.product for item in order.items.all()]).delete()
      elif transaction_status in ['deny', 'cancel', 'expire']:
        order.status = 'Failed'
      order.save()
      return JsonResponse({'status': 'success'})
    except Order.DoesNotExist:
      return JsonResponse({'status': 'error', 'message': 'Order not found'}, status=404)
  return JsonResponse({'status': 'error'}, status=400)