from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import CharField, DecimalField, IntegerField # this is use for create model
from django.db.models.fields.related import ForeignKey
from django.db.models.fields.files import ImageField
from django.db.models.fields import DateTimeField
from django.db.models import OneToOneField, ManyToManyField



# Create your models here.

class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(null=True, blank=True, default='/image/placeholder.png', upload_to='images/')
    image_url = models.URLField(max_length=500, null=True, blank=True)  # New field for storing image URLs
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=1000, null=True, blank=True)
    rating = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return f"{self.name} {self.brand} {self.price}"

    

class Review(models.Model):
    product = ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = CharField(max_length=200, null=True, blank=True)
    rating = IntegerField(null=True, blank=True, default=0)
    comment = CharField(max_length=200, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True) 
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)
    
class Order(models.Model):
    user = ForeignKey(User, on_delete=models.SET_NULL, null=True)
    paymentMethod = CharField(max_length=200, null=True, blank=True)
    taxPrice = DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    isDelivered = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)
    

class OrderItem(models.Model):
    product = ForeignKey(Product, on_delete=models.CASCADE, null=True)
    order = ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    name = CharField(max_length=200, null=True, blank=True)
    qty = IntegerField(null=True, blank=True, default=0)
    price = DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    image = CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return self.name 
    
class ShippingAddress(models.Model):
    order= OneToOneField(Order,on_delete=models.CASCADE,null=True)
    address=CharField(max_length=200,null=True,blank=True)
    city=CharField(max_length=200,null=True,blank=True)
    postalCode=CharField(max_length=200,null=True,blank=True) 
    country=CharField(max_length=200,null=True,blank=True)
    shippingPrice=DecimalField(max_digits=7,decimal_places=2,null=True,blank=True)
    _id=models.AutoField(primary_key=True,editable=False)

    def __str__(self):
        return str(self.address)
