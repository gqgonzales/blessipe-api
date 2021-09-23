from django.db import models
from blessipeapi.models.restaurant import Restaurant
from blessipeapi.models.traveler import Traveler


class Favorite(models.Model):
    """Initializing the Favorite class"""
    traveler = models.ForeignKey(
        "Traveler", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE)
