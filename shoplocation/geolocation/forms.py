from django import forms
from django.contrib.gis.geos import Point

from geolocation.models import Shop

class LocationForm(forms.Form):
    """
    form for input locations
    """
    longitude = forms.DecimalField(max_digits=9, decimal_places=6)
    latitude = forms.DecimalField(max_digits=9, decimal_places=6)
    radius = forms.IntegerField()


class ShopEntryForm(forms.ModelForm):
    name = forms.CharField(max_length=200)
    address = forms.CharField(max_length=100)
    city = forms.CharField(max_length=50)

    latitude = forms.DecimalField(
        min_value=-90,
        max_value=90,
        required=True,
    )
    longitude = forms.DecimalField(
        min_value=-180,
        max_value=180,
        required=True,
    )

    class Meta(object):
        model = Shop
        exclude = []
        widgets = {'point': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        if args:  # If args exist
            data = args[0]
            if data['latitude'] and data['longitude']:  # If lat/lng exist
                latitude = float(data['latitude'])
                longitude = float(data['longitude'])
                mutable = data._mutable
                data._mutable = True
                data['location'] = Point(longitude, latitude, srid=4326)  # Set PointField
                data._mutable = mutable
        try:
            coordinates = kwargs['instance'].point.tuple  # If PointField exists
            initial = kwargs.get('initial', {})
            initial['latitude'] = coordinates[0]  # Set Latitude from coordinates
            initial['longitude'] = coordinates[1]  # Set Longitude from coordinates
            kwargs['initial'] = initial
        except (KeyError, AttributeError):
            pass
        super().__init__(*args, **kwargs)