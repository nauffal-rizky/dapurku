# core/utils/analytics.py
from django.db.models import Sum, Count, Avg
from decimal import Decimal

def get_umkm_dashboard_data(user):
  """Return metrics for UMKM users."""
  products = user.product_set.all()
  total_products = products.count()
  total_sales = products.aggregate(total=Sum('sold'))['total'] or 0
  total_revenue = sum(p.sold * p.price for p in products)
  average_rating = products.aggregate(avg=Avg('rating'))['avg'] or Decimal('0.00')
  top_products = products.order_by('-sold')[:5]

  return {
    'total_products': total_products,
    'total_sales': total_sales,
    'total_revenue': total_revenue,
    'average_rating': round(average_rating, 2),
    'top_products': top_products,
  }

def get_customer_dashboard_data(user):
  """Return metrics for regular customers."""
  orders = user.order_set.all()
  total_orders = orders.count()
  total_items = orders.aggregate(total=Sum('quantity'))['total'] or 0
  total_spent = sum(o.product.price * o.quantity for o in orders)
  favorite_category = (
    orders.values('product__category')
    .annotate(total=Count('product__category'))
    .order_by('-total')
    .first()
  )
  
  return {
    'total_orders': total_orders,
    'total_items': total_items,
    'total_spent': total_spent,
    'favorite_category': favorite_category['product__category'] if favorite_category else "N/A",
  }
