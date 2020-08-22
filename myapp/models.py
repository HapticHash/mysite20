from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
import datetime
from django.contrib.auth.models import User
from django.db.models import Sum
from django.utils import timezone
# Create your models here.

class Topic(models.Model):
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=200, blank= False, default= 'new')

    def __str__(self):
        return self.name

class Course(models.Model):
    topic = models.ForeignKey(Topic, related_name='courses', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    hours = models.IntegerField(default= 40.00)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MaxValueValidator(200), MinValueValidator(100)])
    for_everyone = models.BooleanField(default=True)
    description = models.TextField(max_length=300, null=True, blank=True)
    optional = models.TextField(blank=True)
    interested = models.PositiveIntegerField(default=0)
    stages = models.PositiveIntegerField(default=3)

    def __str__(self):
        return str(self.id) + self.name

    def discount(self):
        return self.price*0.9

class Student(User):
    CITY_CHOICES = [('WS', 'Windsor'),
                    ('CG', 'Calgery'),
                    ('MR', 'Montreal'),
                    ('VC', 'Vancouver')]
    address = models.CharField(max_length=50, null=True, blank=True)
    school = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=2, choices=CITY_CHOICES, default='WS')
    interested_in = models.ManyToManyField(Topic)
    # image = models.ImageField(upload_to='images/', null=True, blank=True)
    def __str__(self):
        return self.first_name + self.last_name



class Order(models.Model):
    courses = models.ManyToManyField(Course)
    Student = models.ForeignKey(Student, on_delete=models.CASCADE)
    levels = models.PositiveIntegerField(default=0)
    ORDER_STATUSES = [('0', 'Cancelled'),
                      ('1', 'Order Confirmed')]
    order_status = models.CharField(max_length=2, null=True, choices=ORDER_STATUSES, default='1')
    order_date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return str(self.id) + self.Student.first_name + self.Student.last_name

    def total_cost(self):
        return Course.objects.aggregate(Sum('price'))

class Feedback(models.Model):
    student = models.ForeignKey(Student, related_name='feedback_from', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    suggestions = models.CharField(max_length=200)