from django.core import serializers
from ..models import Events, MapDealers, Events_Tuscany
from django.http import HttpResponse

# api for Shelby events
def eventsAPI(request):
    obj = Events.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")

# api for Shelby mapdealers
def mapdealersAPI(request):
    obj = MapDealers.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")

# api for Tuscany events
def eventsTuscanyAPI(request):
    obj = Events_Tuscany.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")

# api for Tuscany mapdealers < model not implemented
# def mapdealersTuscanyAPI(request):
#     obj = MapDealers.objects.all()
#     serialized_obj = serializers.serialize("json", obj)
#     print(serialized_obj)
#     return HttpResponse(serialized_obj, content_type="application/json")