from django.db import models
from django.contrib.auth.models import User


class Traveler(models.Model):
    """initializing the traveler module"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=80)
    # city = models.ForeignKey("City", on_delete=models.CASCADE)

    @property
    def full_name(self):
        """returns auth user full name"""
        return f'{self.user.first_name} {self.user.last_name}'

    def __str__(self):
        return self.user.get_full_name()
