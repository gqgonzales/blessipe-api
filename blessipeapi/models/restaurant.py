from django.db import models
from django.db.models.fields import CharField


class Restaurant(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=75)
    phone_number = CharField(max_length=16)
    url = models.URLField()
    city = models.ForeignKey(
        "City", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} in {self.city.name}'
