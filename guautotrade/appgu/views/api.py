from django.core import serializers
from ..models import Events, MapDealers
from django.http import HttpResponse

# api for events
def eventsAPI(request):
    obj = Events.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")

# api for mapdealers
def mapdealersAPI(request):
    obj = MapDealers.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")

