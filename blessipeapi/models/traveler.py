from django.db import models
from django.contrib.auth.models import User


class Traveler(models.Model):
    """initializing the traveler module"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=80)
    # city = models.ForeignKey("City", on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
