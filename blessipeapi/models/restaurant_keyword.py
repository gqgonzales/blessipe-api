from blessipeapi.models.restaurant import Restaurant
from blessipeapi.models.keyword import Keyword
from django.db import models


class RestaurantKeyword(models.Model):
    """
    Keywords attatched to restaurants
    """
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    keyword = models.ForeignKey("Keyword", on_delete=models.CASCADE)
