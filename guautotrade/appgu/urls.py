from django.urls import include, path

from . import views
from django.contrib.auth.views import login

urlpatterns = [
    path('', views.index, name='index'),
	path('dealerlogin/', login, {'template_name': 'dealerportal/dealerlogin.html'}),
	path('dealerlogin/order', views.dealerportal, name='dealerportal'),
	path('dealerlogin/orderlist', views.orderlist, name='orderlist'),
	path('dealerlogin/registerdealer', views.registerdealer, name='registerdealer'),
	path('accounts/', include('django.contrib.auth.urls')),
	path('shelby/', views.shelby, name='shelby'),
	path('shelby/contact/', views.contact, name='contact'),
	path('shelby/vehicle/', views.vehicledesc, name='vehicledesc'),
]