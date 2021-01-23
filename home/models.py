from django.db import models
from geopy.geocoders import Nominatim
from geopy import distance
import numpy as np

# Create LOCATION model
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
    coord_x = models.FloatField()
    coord_y = models.FloatField()

    def get_coords(self):
        '''Returns coordenates from input address.'''
        if self.post_code is not None:
            geolocator = Nominatim(user_agent="picapedro2@gmail.com")  # some email was required
            location = geolocator.geocode(self.post_code)
            self.coord_x = location.latitude
            self.coord_y = location.longitude


# Create PRODUCT model
class Product(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField()


# Create COMPANY model
class Company(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=200)
    bio = models.TextField(max_length=1000)


class CompanyManager(models.Manager):

    def proximity_search(self, loc, others):
        """Input:
           loc     = List with your coordinates [x,y]
           others  = List with other coordinates. [[x1,y1],[x2,y2],...]

           Return:
           distances
           ordered distances
           shortest distance
           index location of shortest distance in others
           """

        res = []

        for i in range(len(others)):
            others_i = tuple(others[i])

            res.append(distance.distance(loc, others_i).miles)

        # res is the distances
        # quicksort res
        def sort(array):
            """Sort the array by using quicksort."""

            less = []
            equal = []
            greater = []

            if len(array) > 1:
                pivot = array[0]
                for x in array:
                    if x < pivot:
                        less.append(x)
                    elif x == pivot:
                        equal.append(x)
                    elif x > pivot:
                        greater.append(x)
                # Don't forget to return something!
                return sort(less) + equal + sort(greater)  # Just use the + operator to join lists
            # Note that you want equal ^^^^^ not pivot
            else:  # You need to handle the part at the end of the recursion - when you only have one element in your array, just return the array.
                return array

        ordered = sort(res)

        # list of index locations of "ordered" objects in "res"
        indices = [res.index(ordered[j]) for j in range(len(ordered))]

        nearest = [others[i] for i in indices]

        return nearest

    def nearby(self, coords, limit):
        """
        Returns the companies that are nearby to the given coordinates with a limit on the number of companies returned.
        """
        # get all possible coordinates
        all_coords = []
        for company in Company.objects.all():
            all_coords.append([company.coord_x, company.coord_y])

        # compute nearest n coordinates
        nearest = self.proximity_search(coords, all_coords)

        # get closest n
        nearest_limit = nearest[:limit]

        # iterate over nearest_limit and populate
        dummy_nearest = [None for i in range(limit)]
        for company in Company.objects.all():
            coords = [company.coord_x, company.coord_y]
            index = np.where(np.all(coords == nearest_limit))
            if index is not None:
                dummy_nearest[index] = company

        return dummy_nearest
