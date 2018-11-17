from django import template
from collections import OrderedDict
from ..models import Vehicles, MapDealers
from django_countries import countries
import urllib.request, json, threading
from urllib.request import urlopen
import queue

register = template.Library()
api_list = []
country_dealers = {}
dic = {}

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

    for i in map:
        if i.country not in country_dealers:
            country_dealers[i.country] = []
        country_dealers[i.country].append(i.customer_name)


    for country in country_dealers:
        api_list.append(country)
        # api_list[country] = urlx + country

    fetch_parallel()

    # for x in country_dealers:
    #     with urllib.request.urlopen(urlx + x) as url:
    #         print(urlx + x)
    #         data = json.loads(url.read().decode())

            # region = data['region']
            # if region == 'Americas':
            #     region = data['subregion']

            # if region not in dic:
            #     dic[region] = {}
            # dic[region][dict(countries)[x]] = country_dealers[x]

    sortedlist = OrderedDict()

    # sort continents
    sortedcontinent = sorted(dic, key=str.lower)

    for continent in sortedcontinent:
        orderedlist = sorted(dic[continent], key=str.lower)
        sortedlist[continent] = OrderedDict()
        for country in orderedlist:
            sortedlist[continent][country] = dic[continent][country]

    return sortedlist
    # print("FINAL PRINT")
    # print(dic)
    # return dic

def fetch_parallel():
    result = queue.Queue()
    threads = [threading.Thread(target=read_url, args = (urlcode,result)) for urlcode in api_list]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return result

def read_url(urlcode, queue):
    url = 'https://restcountries.eu/rest/v2/alpha/' + urlcode  
    # data = urlopen(url).read()
    data = json.loads(urlopen(url).read().decode())

    region = data['region']
    if region == 'Americas':
        region = data['subregion']

    if region not in dic:
        dic[region] = {}
    dic[region][dict(countries)[urlcode]] = country_dealers[urlcode]
    # dic["europe"][dict(countries)["UK"]] = country_dealers["UK"]
    # print(dict(countries))
    # print(data)
    queue.put(data)