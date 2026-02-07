from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

# Import all views you need
from . import views

urlpatterns = [
  path('frontpage/', views.frontPage, name = "frontpage"),
  path('login/', views.loginPage, name = "login"),
  path('logout/', views.logoutUser, name = "logout"),
  path('signup/', views.signupPage, name = "signup"),
  path('about/', views.aboutPage, name = "about"),
  path('profile/', views.profilePage, name = "profile"),
  path('umkm/profile/<int:user_id>/', views.umkmProfilePage, name = "umkm_profile"),

  path('', views.productPage, name = "products"),
  path('<int:pk>', views.productDetailPage, name = "product_detail"),

  path("umkm/product/add", views.manage_product, name="add_product"),
  path("umkm/product/<int:pk>/", views.manage_product, name="edit_product"),
  path("umkm/product/<int:pk>/delete/", views.delete_product, name="delete_product"),

  path('order/', views.orderPage, name = "order"),
  path('order/list/', views.order_list, name='order_list'),
  path('order/list/<int:order_id>/', views.order_detail, name='order_detail'),
  
  path('cartpage/', views.cartPage, name = "cart"),
  path('cartpage/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
  path('update-cart-item/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
  path('cartpage/delete_item/<int:cart_item_id>/', views.delete_cart_item, name='delete_cart_item'),
  path('cartpage/create_order/', views.create_order, name='create_order'),

  path("contact/", views.contactPage, name="contact"),

  path("address/add/", views.add_address, name="add_address"),
  path("address/update/<int:address_id>/", views.update_address, name="update_address"),
  path("address/delete/<int:address_id>/", views.delete_address, name="delete_address"),
]

if settings.DEBUG:
  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
