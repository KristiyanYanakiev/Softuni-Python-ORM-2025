import os
import django
from django.db.models import Q, Count, F

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from populate_dp import populate_model_with_data

# Import your models here
from main_app.models import Profile, Order, Product


# Create queries within functions
def populate_db() -> None:
    populate_model_with_data(Profile)
    populate_model_with_data(Product)
    populate_model_with_data(Order)



def get_profiles(search_string=None) -> str:
    profiles = Profile.objects.filter(
        Q(full_name__istartswith=search_string) | Q(full_name__iendswith=search_string) |
        Q(full_name__icontains=search_string) | Q(email__istartswith=search_string) | Q(email__iendswith=search_string) | Q(email__icontains=search_string)
        | Q(phone_number__istartswith=search_string) | Q(phone_number__iendswith=search_string) | Q(phone_number__icontains=search_string) ).order_by('full_name')

    if not profiles.exists():
        return ''
    else:
        return '\n'.join(f"Profile: {p.full_name}, email: {p.email}, phone number: {p.phone_number}, orders: {p.order_set.count}" for p in profiles)

def get_loyal_profiles():
    profiles = Profile.objects.annotate(num_orders=Count('order')).filter(num_orders__gt=2).order_by('num_orders')

    if not profiles.exists():
        return ''
    else:
        return '\n'.join(f"Profile: {p.full_name}, orders: {p.num_orders}" for p in profiles)

def get_last_sold_products():
    last_order = Order.objects.all().order_by('creation_date').last()
    if not last_order:
        return ''
    products = last_order.products.all().order_by('name')
    products_name = ', '.join(f"{p.name}" for p in products)
    if not products.exists():
        return ''
    else:
        return f"Last sold products: {products_name}"


def get_top_products():
    top_5_products = Product.objects.annotate(order_count=Count('order')).order_by('-order_count', 'name')[:5]
    if not top_5_products.exists():
        return ''

    res = []
    res.append('Top products:\n')
    res.append('\n'.join(f"{p.name}, sold {p.order_count} times" for p in top_5_products if p.order_count >0))

    return ''.join(res)


def apply_discounts():
    orders =  Order.objects.annotate(products_count=Count('products')).filter(products_count__gt=2, products__order__is_completed=False)
    num_of_updated_orders = 0 if not orders.exists() else orders.count()
    Product.objects.filter(order__in=orders).update(price=F('price') * 0.9)

    return f"Discount applied to {num_of_updated_orders} orders."

def complete_order():
    order = Order.objects.filter(is_completed=False).order_by('-creation_date').first()

    if not order:
        return ''

    order.is_completed = True
    order.save()
    for p in order.products.all():
        p.in_stock -= 1
        if p.in_stock == 0:
            p.is_available = False

    return "Order has been completed!"







