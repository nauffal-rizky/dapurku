# umkm/utils.py
from users_db.models import Product, Order

def get_umkm_dashboard_data(user):
  """Return summary data for UMKM dashboard."""
  products = Product.objects.filter(umkm_user_id=user)
  total_products = products.count()
  total_stock = sum(p.stock for p in products if hasattr(p, "stock"))
  return {
    "total_products": total_products,
    "total_stock": total_stock,
  }

def get_customer_dashboard_data(user):
  """Return summary data for regular customer dashboard."""
  orders = Order.objects.filter(customer=user)
  total_orders = orders.count()
  total_spent = sum(o.total_price for o in orders)
  return {
    "total_orders": total_orders,
    "total_spent": total_spent,
  }
