from django.db import models
from django.db.models.fields import CharField
from phonenumber_field.modelfields import PhoneNumberField


class Restaurant(models.Model):

    name = models.CharField(max_length=100)
    address = models.CharField(max_length=75)
    phone_number = PhoneNumberField()
    url = models.URLField()
    city = models.ForeignKey(
        "City", on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} in {self.city.name}'
