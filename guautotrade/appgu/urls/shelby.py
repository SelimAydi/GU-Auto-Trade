from django.urls import path
from appgu.oscar_urls import application
from ..views import shelby
# from paypal.express.dashboard.app import application

urlpatterns = [
    path('', shelby.index, name='shelby'),
    path('dealers/', shelby.dealers, name='dealers'),
    path('events/', shelby.events, name='events'),
    path('shop/', application.urls),
    path('news/', shelby.news, name='news'),
    path('media/', shelby.pressandmedia, name='pressandmedia'),
    path('contact/', shelby.contact, name='contact'),
    path('vehicle/', shelby.vehicledesc, name='vehicledesc'),
]