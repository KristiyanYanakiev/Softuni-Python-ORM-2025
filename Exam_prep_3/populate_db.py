import random
from _decimal import Decimal

from django.db.models import (
    AutoField, PositiveIntegerField, PositiveSmallIntegerField,
    BooleanField, CharField, TextField, EmailField,
    DecimalField, DateField, IntegerField, FloatField
)
from django.db.models.fields.related import ForeignKey, OneToOneField

from datetime import datetime, timedelta


def populate_model_with_data(model, num_records=10):
    model_fields = model._meta.fields
    many_to_many_fields = model._meta.local_many_to_many

    for i in range(num_records):
        field_values = {}

        for field in model_fields:

            # Handle choices
            if hasattr(field, 'choices') and field.choices:
                field_values[field.name] = random.choice(field.choices)[0]

            elif isinstance(field, AutoField):
                continue

            # Positive integer fields
            elif isinstance(field, PositiveIntegerField) or isinstance(field, PositiveSmallIntegerField):
                field_values[field.name] = random.randint(1, 100)

            # Normal integer fields
            elif isinstance(field, IntegerField):
                field_values[field.name] = random.randint(-100, 100)

            # Boolean
            elif isinstance(field, BooleanField):
                field_values[field.name] = random.choice([True, False])

            # Float fields (e.g., spacecraft weight)
            elif isinstance(field, FloatField):
                # Minimum value 0.0
                field_values[field.name] = round(random.uniform(0.0, 50000.0), 2)

            # Char and Text fields
            elif isinstance(field, CharField) or isinstance(field, TextField):
                field_values[field.name] = f"{model.__name__} {i+1}"

            # Email
            elif isinstance(field, EmailField):
                field_values[field.name] = f"{random.choice(['user', 'admin', 'pilot'])}@example.com"

            # Decimal fields
            elif isinstance(field, DecimalField):
                random_decimal = random.uniform(1, 10)
                field_values[field.name] = Decimal(f"{random_decimal:.{field.decimal_places}f}")

            # Dates
            elif isinstance(field, DateField):
                start_date = datetime(2000, 1, 1).date()
                end_date = datetime.today().date()
                delta_days = (end_date - start_date).days
                field_values[field.name] = start_date + timedelta(days=random.randint(0, delta_days))

            # Foreign keys
            elif isinstance(field, ForeignKey) or isinstance(field, OneToOneField):
                related_model = field.related_model
                related_instance = related_model.objects.order_by('?').first()

                # If FK is NOT NULL and no object exists yet → create minimal related object
                if related_instance is None and not field.null:
                    related_instance = related_model.objects.create(
                        **{
                            f.name: f"{related_model.__name__} {i+1}"
                            for f in related_model._meta.fields
                            if isinstance(f, CharField) and not f.primary_key
                        }
                    )

                field_values[field.name] = related_instance

        # Create the model instance
        instance = model.objects.create(**field_values)

        # ManyToMany fields (after instance exists)
        for field in many_to_many_fields:
            related_model = field.related_model
            related_instances = related_model.objects.order_by('?')[:random.randint(1, 5)]
            getattr(instance, field.name).set(related_instances)
