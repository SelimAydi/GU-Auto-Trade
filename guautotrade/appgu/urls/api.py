from django.urls import path
from ..views import eventsAPI, mapdealersAPI, eventsTuscanyAPI

urlpatterns = [
    path('shelby/events/', eventsAPI, name='eventsAPI'),
    path('shelby/mapdealers/', mapdealersAPI, name='mapdealersAPI'),
    path('tuscany/events/', eventsTuscanyAPI, name='tuscanyeventsAPI'),
]
