from django.db import models


class City(models.Model):
    """Initializing the City class"""
    name = models.CharField(max_length=100)
    country = models.ForeignKey(
        "Country", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}'
