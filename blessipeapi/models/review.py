from django.db import models
from django.db.models.deletion import CASCADE


class Review(models.Model):
    recipe = models.ForeignKey("recipe", on_delete=CASCADE)
    traveler = models.ForeignKey("Traveler", on_delete=CASCADE)
    restaurant = models.ForeignKey("Restaurant", on_delete=CASCADE)
    date = models.DateField()
    title = models.CharField(max_length=75)
    body = models.TextField()

    def __str__(self):
        return f'{self.title}, a review'
