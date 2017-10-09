from django.shortcuts import render

from django.contrib.gis import geos
from django.contrib.gis import measure
from django.shortcuts import render_to_response
from django.template import RequestContext

from geolocation.forms import LocationForm
from geolocation.models import Shop


def get_shops(longitude, latitude, radius):
    """
    :param longitude:
    :param latitude:
    :param radius:
    :return: List of near the given input longitude, latitude under the given radius.
    """
    current_point = geos.fromstr("POINT(%s %s)" % (longitude, latitude))
    distance_from_point = {'km': radius}

    shops = Shop.gis.filter(location__distance_lte=(current_point,
                                                    measure.D(**distance_from_point)))
    shops = shops.distance(current_point).order_by('distance')
    return shops.distance(current_point)

def home(request):
    """
    View for the geolocation app for shoplocation.
    """
    form = LocationForm()
    shops = []
    if request.POST:
        form = LocationForm(request.POST)
        if form.is_valid():
            longitude = form.cleaned_data['longitude']
            latitude = form.cleaned_data['latitude']
            radius = form.cleaned_data['radius']
            shops = get_shops(longitude, latitude, radius)

    return render(request, 'home.html', {'form': form, 'shops': shops})
