from django.urls import include, path

from . import views
from django.contrib.auth.views import login

urlpatterns = [
    path('', views.index, name='index'),
	path('dealerlogin/', login, {'template_name': 'dealerlogin.html'}),
	path('dealerlogin/order', views.dealerportal, name='dealerportal'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('shelby/', views.shelby, name='shelby'),
	path('shelby/contact/', views.contact, name='contact'),
	path('shelby/vehicle/', views.vehicledesc, name='vehicledesc'),
]