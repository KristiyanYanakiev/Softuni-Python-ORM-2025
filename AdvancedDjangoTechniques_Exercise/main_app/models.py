from decimal import Decimal

from django.core.validators import MinValueValidator, EmailValidator, RegexValidator, URLValidator, MinLengthValidator
from django.db import models

from mixins import RechargeEnergyMixin
from validators import check_spaces_letters_validator


# Create your models here.
class Customer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[check_spaces_letters_validator]
    )
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(limit_value=18, message='Age must be greater than or equal to 18')]
    )
    email = models.EmailField(
        error_messages={'invalid': 'Enter a valid email address'}
    )

    phone_number = models.CharField(
        max_length=13,
        validators=[RegexValidator(r'^\+359\d{9}$', message="Phone number must start with '+359' followed by 9 digits")]
    )
    website_url = models.URLField(
        error_messages={'invalid': 'Enter a valid URL'}
    )


class BaseMedia(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ['-created_at', 'title']


class Book(BaseMedia):
    author = models.CharField(max_length=100, validators=[MinLengthValidator(5, 'Author must be at least 5 characters long')])
    isbn = models.CharField(
        max_length=20,
        unique=True,
        validators=[MinLengthValidator(6, 'ISBN must be at least 6 characters long')]
    )

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Book'
        verbose_name_plural = 'Models of type - Book'


class Movie(BaseMedia):
    director = models.CharField(max_length=100, validators=[MinLengthValidator(8, 'Director must be at least')])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Movie'
        verbose_name_plural = 'Models of type - Movie'

class Music(BaseMedia):
    artist = models.CharField(max_length=100,
                              validators=[MinLengthValidator(9, 'Artist must be at least 9 characters long')])

    class Meta(BaseMedia.Meta):
        verbose_name = 'Model Music'
        verbose_name_plural = 'Models of type - Music'


class Product(models.Model):
    TAX_RATE_PERCENTAGE = Decimal('0.8')
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def calculate_tax(self) -> Decimal:
        return Decimal(str(self.price * self.TAX_RATE_PERCENTAGE))

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        shipping_cost = float(weight) * 2.00
        return Decimal(str(shipping_cost))

    def format_product_name(self) -> str:
        return f"Product: {self.name}"



class DiscountedProduct(Product):
    TAX_RATE_PERCENTAGE = Decimal('0.5')
    class Meta:
        proxy = True

    def calculate_price_without_discount(self) -> Decimal:
        price_without_discount = float(self.price) * 1.20
        return Decimal(str(price_without_discount))

    def calculate_tax(self) -> Decimal:
        return Decimal(str(self.price * self.TAX_RATE_PERCENTAGE))

    def calculate_shipping_cost(self, weight: Decimal) -> Decimal:
        return Decimal(str(float(weight) * 1.5))

    def format_product_name(self) -> str:
        return f"Discounted Product: {self.name}"


class Hero(RechargeEnergyMixin):
    name = models.CharField(max_length=100)
    hero_title = models.CharField(max_length=100)
    energy = models.PositiveIntegerField()


class SpiderHero(Hero):
    def swing_from_buildings(self) -> str:
        if self.energy < 80:
            return f"{self.name} as Spider Hero is out of web shooter fluid"
        self.energy -= 80
        if self.energy == 0:
            self.energy = 1
            self.save()

        return f"{self.name} as Spider Hero swings from buildings using web shooters"

    class Meta:
        proxy = True

class FlashHero(Hero):
    def run_at_super_speed(self) -> str:
        if self.energy < 65:
            return f"{self.name} as Flash Hero needs to recharge the speed force"
        self.energy -= 65
        if self.energy == 0:
            self.energy = 1
            self.save()

        return f"{self.name} as Flash Hero runs at lightning speed, saving the day"

    class Meta:
        proxy = True
