from django.db import models


class RecipeComment(models.Model):
    """Comment model
    fields:
        post (ForeignKey): the post associated with the comment
        author (ForeignKey): the user that made the comment
        body (TextField): text field for comment
        date_created (DateTimeField): the date of a comment
    """
    recipe = models.ForeignKey("Recipe", on_delete=models.CASCADE)
    author = models.ForeignKey("Traveler", on_delete=models.CASCADE)
    body = models.TextField()
    date_created = models.DateTimeField()

    @property
    def owner(self):
        return self.__owner

    @owner.setter
    def owner(self, value):
        self.__owner = value
