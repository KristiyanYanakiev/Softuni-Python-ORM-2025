from django.db import models

class Student(models.Model):
    student_id = models.CharField(max_length=10, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Employee(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    department = models.CharField(max_length=100)
    salary = models.PositiveIntegerField()

    def __str__(self):
        return (f"{self.first_name} {self.last_name} from department: {self.department} with "
                f"salary: {self.salary}")

