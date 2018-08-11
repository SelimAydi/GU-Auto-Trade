from django.urls import path
# from .. import views
from ..views import eventsAPI, mapdealersAPI

urlpatterns = [
    path('events/', eventsAPI, name='eventsAPI'),
    path('mapdealers/', mapdealersAPI, name='mapdealersAPI'),
]