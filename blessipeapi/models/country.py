from django.db import models


class Country(models.Model):
    """Initializing the City class"""
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name}'
