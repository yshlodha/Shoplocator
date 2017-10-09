from django.conf.urls import url

from geolocation.views import home


urlpatterns = [
    url(r'^shop/', home, name='home'),
]