from django import template
from ..models import Vehicles

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
