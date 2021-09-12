from django.db import models
from django.db.models.deletion import CASCADE


class Rating(models.Model):
    restaurant = models.ForeignKey("Restaurant", on_delete=CASCADE)
    traveler = models.ForeignKey("Traveler", on_delete=CASCADE)
    recipe = models.ForeignKey("Recipe", on_delete=CASCADE)
    rating = models.IntegerField()

    def __str__(self):
        return f'{self.rating}/5 Stars'
