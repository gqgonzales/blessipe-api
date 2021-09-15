from django.contrib import admin
from blessipeapi.models import Traveler, Country, City, Restaurant, Recipe, Keyword, RecipeKeyword, RestaurantKeyword

# Register your models here.
admin.site.register(Traveler)
admin.site.register(Country)
admin.site.register(City)
admin.site.register(Restaurant)
admin.site.register(Recipe)
admin.site.register(Keyword)
admin.site.register(RecipeKeyword)
admin.site.register(RestaurantKeyword)
