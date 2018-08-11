from django.urls import path
from ..views import tuscany

urlpatterns = [
    path('', tuscany.index, name='tuscany'),
    path('dealers/', tuscany.dealers, name='dealers'),
    path('events/', tuscany.events, name='events'),
    path('shop/', tuscany.shop, name='shop'),
    path('news/', tuscany.news, name='news'),
    path('contact/', tuscany.contact, name='contact'),
    path('vehicle/', tuscany.vehicledesc, name='vehicledesc'),
]