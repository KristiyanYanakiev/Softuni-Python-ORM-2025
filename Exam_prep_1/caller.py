import os
import django
from django.db.models import Q, Count

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

