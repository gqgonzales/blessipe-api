from django.db import models


class Recipe(models.Model):
    restaurant = models.ForeignKey(
        "Restaurant", on_delete=models.CASCADE)
    traveler = models.ForeignKey(
        "Traveler", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    date = models.DateField()
    image = models.ImageField(upload_to='recipeimages', height_field=None,
                              width_field=None, max_length=None, null=True)
    keywords = models.ManyToManyField(
        "Keyword", through="RecipeKeyword", related_name="recipe_keywords", blank=True)

    # comments = models.TextField()

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        self.__author = value

    def __str__(self):
        return f'{self.name} from {self.restaurant.name}'
