from django.urls import path
from django.contrib.auth.views import login
from ..views import portal

urlpatterns = [
    path('', login, {'template_name': 'portal/index.html'}),
    # path('', portal.index, name='index'),
    path('search/', portal.search, name='search'),
    path('order/', portal.order, name='portalorder'),
    path('addvehicle/', portal.addvehicle, name='upload'),
    path('addnewspost/', portal.addnewspost, name='newspost'),
    path('addeventpost/', portal.addeventpost, name='eventpost'),
    path('addmapdealer/', portal.addmapdealer, name='mapdealer'),
    path('myorders/', portal.portalmyorders, name='myorders'),
    path('orderlist/', portal.portalorderlist, name='orderlist'),
    path('registerdealer/', portal.registerdealer, name='registerdealer'),
    path('registeradmin/', portal.registeradmin, name='registeradmin'),
    path('changepassword/', portal.changePassword, name='changepassword'),
]