
from django.db.models.fields import related
from blessipeapi.models.traveler import Traveler
from django.db import models
from django.db.models.deletion import CASCADE


class RecipeImage(models.Model):
    recipe = models.ForeignKey("Recipe", on_delete=CASCADE)
    traveler = models.ForeignKey("Traveler", on_delete=CASCADE)
    image = models.ImageField(upload_to='recipeimages', height_field=None,
                              width_field=None, max_length=None, null=True)
