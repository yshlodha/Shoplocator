from django.contrib.gis.db import models as gis_models
from django.contrib.gis import geos
from django.db import models



class Shop(models.Model):
    """
    Shops model to store shop details like shop name city and location etc.
    """
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    location = gis_models.PointField(u"longitude/latitude", geography=True, srid=4326, blank=True, null=True)

    gis = gis_models.GeoManager()
    objects = models.Manager()

    def __str__(self):
        return self.name
