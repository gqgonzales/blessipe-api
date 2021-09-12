from blessipeapi.models.recipe import Recipe
from django.db import models


class RecipeKeyword(models.Model):
    """
    Keywords attatched to recipes
    """
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    keyword = models.ForeignKey("Keyword", on_delete=models.CASCADE)
    