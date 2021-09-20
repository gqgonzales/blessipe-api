"""blessipe URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.conf.urls import include
from django.urls import path
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static
from blessipeapi.views import register_user, login_user, RecipeView, RestaurantView, CountryView, CityView, TravelerView, ProfileView, KeywordView, RecipeKeywordView, RestaurantKeywordView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'profiles', ProfileView, 'profile')
router.register(r'travelers', TravelerView, 'traveler')
router.register(r'recipes', RecipeView, 'recipe'),
router.register(r'restaurants', RestaurantView, 'restaurant'),
router.register(r'countries', CountryView, 'country')
router.register(r'cities', CityView, 'city')
router.register(r'keywords', KeywordView, 'keyword')
router.register(r'recipekeywords', RecipeKeywordView, 'recipekeyword')
router.register(r'restaurantkeywords',
                RestaurantKeywordView, 'restaurantkeyword')

urlpatterns = [
    path('', include(router.urls)),
    path('register', register_user),
    path('login', login_user),
    path('api-auth', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
