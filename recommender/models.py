from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    price = models.FloatField()
    lifecycle_years = models.IntegerField()
    stock = models.IntegerField()
    tags = models.TextField()

class Sale(models.Model):
    user_id = models.IntegerField()
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    purchase_date = models.DateField()
    payment_method = models.CharField(max_length=50)