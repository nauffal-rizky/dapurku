from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path('', views.frontPage, name = "frontpage"),
  path('login/', views.loginPage, name = "login"),
  path('logout/', views.logoutUser, name = "logout"),
  path('signup/', views.signupPage, name = "signup"),
  path('about/', views.aboutPage, name = "about"),
  path('profile/', views.profilePage, name = "profile"),
  path('umkm/profile/<int:user_id>/', views.umkmProfilePage, name = "umkm_profile"),
  path('products/', views.productPage, name = "products"),
  path('products/<int:pk>', views.productDetailPage, name = "product_detail"),
  path('umkm/add-product/', views.addProduct, name='add_product'),
  path('umkm/edit-product/<int:pk>/', views.editProduct, name='edit_product'),
  path('umkm/delete-product/<int:pk>/', views.deleteProduct, name='delete_product'),
  path('order/', views.orderPage, name = "order"),
  path('cartpage/', views.cartPage, name = "cart"),
  path("cartpage/add/<int:product_id>/", views.addToCart, name="cartNewProduct"),
  path("cartpage/add/<int:product_id>/<int:variant_id>/", views.addToCart, name="cartNewVariant"),
  path('contact/', views.contactPage, name = "contact"),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)