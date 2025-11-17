from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator
from django.db import models
from django.db.models import Count

class CreationDateFieldMixin(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class ProfileManager(models.Manager):
    def get_regular_customers(self):
        return self.annotate(num_orders = Count('order')).order_by('-num_orders')


# Create your models here.
class Profile(CreationDateFieldMixin):
    full_name = models.CharField(max_length=100, validators=[MinLengthValidator(2)])
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    objects = ProfileManager()



class Product(CreationDateFieldMixin):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    in_stock = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    is_available = models.BooleanField(default=True)



class Order(CreationDateFieldMixin):
    profile = models.ForeignKey(to=Profile, on_delete=models.CASCADE )
    products = models.ManyToManyField(to=Product)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.01)])
    is_completed = models.BooleanField(default=False)

