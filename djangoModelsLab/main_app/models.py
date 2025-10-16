from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=30)
    email_address = models.EmailField()
    photo = models.URLField()
    birth_date = models.DateField()
    works_full_time = models.BooleanField(default=False)
    created_on = models.DateField(auto_now_add=True)

class Department(models.Model):

    class Cities(models.TextChoices):
        SF = 'Sf', 'Sofia',
        PD = 'Pd', 'Plovdiv'
        V = 'V', 'Varna'
        BS = 'Bs', 'Burgas'


    code = models.CharField(
        max_length=4,
        primary_key=True,
        unique=True
    )
    name = models.CharField(max_length=50, unique=True)
    employees_count = models.PositiveIntegerField(
        default=1,
        verbose_name='Employees Count'
    )
    location = models.CharField(
        max_length=20,
        null=True,
        choices=Cities.choices
    )
    last_edited_on = models.DateTimeField(
        auto_now=True,
        editable=False
    )