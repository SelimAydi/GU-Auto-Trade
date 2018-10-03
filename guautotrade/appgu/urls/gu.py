from django.urls import path
from appgu.oscar_urls import application
from ..views import gu

urlpatterns = [
    path('', gu.index, name='gu'),
    path('about', gu.about, name='about'),
    path('contact', gu.contact, name='contact'),
    path('services', gu.services, name='services'),
]