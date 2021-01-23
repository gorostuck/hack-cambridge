from django.db import models
from geopy import Nominatim


class Location(models.Model):

    def get_coords(post_code):
        '''Returns coordenates from input address.'''
        geolocator = Nominatim(user_agent="picapedro2@gmail.com")  # some email was required
        location = geolocator.geocode(post_code)
        return [location.latitude, location.longitude]

    street = models.CharField(max_length=200)
    number = models.IntegerField()
    other = models.IntegerField()
    country = models.CharField(max_length=200)
    post_code = models.CharField(max_length=200)
    coord_x = get_coords(post_code)[0]
    coord_y = get_coords(post_code)[1]


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


class CompanyManager(models.Manager):
    def nearby(self, coords, limit):
        # Returns the companies that are nearby to the given coordinates,
        # with a limit on the number of companies returned
        return None
