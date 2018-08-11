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
        print("no vehicles")
        return False
    print("yes vehicles")
    return True

@register.simple_tag()
def getCountry():
    map = MapDealers.objects.all()
    for i in map:
        print(i.country)
    urlx = "https://restcountries.eu/rest/v2/alpha/"

    lst = {}
    newlst = []
    dic = {}

    for i in map:
        if i.country not in lst:
            # lst.append(i.country)
            lst[i.country] = []
        lst[i.country].append(i.customer_name)


    for x in lst:
        with urllib.request.urlopen(urlx + x) as url:
            data = json.loads(url.read().decode())

            region = data['region']
            if region == 'Americas':
                region = data['subregion']
                print("is Americas")

            # lst.append(data['region'])
            if region not in dic:
                print("NOT")
                dic[region] = {}
            # dic[region].append(dict(countries)[x])
            dic[region][dict(countries)[x]] = lst[x]
            # dic[data['region']] = []


    # region = data['region']
    print("dic", dic)
    print("list", lst)

    # x = dict(countries)
    # print(x)
    return dic