from django import template
from ..models import Vehicles, MapDealers
from django_countries import countries
import urllib.request, json

register = template.Library()

@register.filter
def stripslashes(url):
    return url.replace('/', '')

@register.simple_tag()
def vehiclesExist():
    vehicle_list = Vehicles.objects.all()
    if len(vehicle_list) == 0:
        return False
    return True

@register.simple_tag()
def getCountry():
    map = MapDealers.objects.all()
    urlx = "https://restcountries.eu/rest/v2/alpha/"

    lst = {}
    newlst = []
    dic = {}

    for i in map:
        if i.country not in lst:
            lst[i.country] = []
        lst[i.country].append(i.customer_name)


    for x in lst:
        with urllib.request.urlopen(urlx + x) as url:
            data = json.loads(url.read().decode())

            region = data['region']
            if region == 'Americas':
                region = data['subregion']

            if region not in dic:
                dic[region] = {}
            dic[region][dict(countries)[x]] = lst[x]

    return dic