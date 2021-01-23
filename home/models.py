from django.db import models


# Create LOCATION model
class Location(models.Model):
    street = models.CharField(max_length=200)
    number = models.IntegerField()
    other = models.IntegerField()
    country = models.CharField(max_length=200)
    post_code = models.CharField(max_length=200)


# Create PRODUCT model
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()


# Create COMPANY model
class Company(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=1000)