from django import template
from collections import OrderedDict
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

    sortedlist = OrderedDict()

    # sort continents
    sortedcontinent = sorted(dic, key=str.lower)

    for continent in sortedcontinent:
        orderedlist = sorted(dic[continent], key=str.lower)
        sortedlist[continent] = OrderedDict()
        for country in orderedlist:
            sortedlist[continent][country] = dic[continent][country]

    return sortedlist