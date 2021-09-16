from django.db import models


class Recipe(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE)
    traveler = models.ForeignKey(
        "Traveler", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    date = models.DateField()
    # image = models.ForeignKey("RecipeImage", on_delete=models.CASCADE)
    # comments = models.TextField()

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    def __str__(self):
        return self.name
