from django.urls import include, path

from . import views
from django.contrib.auth.views import login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('portal/', login, {'template_name': 'dealerportal/dealerlogin.html'}),
    path('portal/order/', views.dealerportalorder, name='dealerportal'),
    path('portal/order/status/', views.status, name='status'),
    path('portal/addvehicle/', views.addvehicle, name='upload'),
    path('portal/myorders/', views.dealerportalmyorders, name='myorders'),
    path('portal/orderlist/', views.dealerportalorderlist, name='orderlist'),
    path('portal/registerdealer/', views.registerdealer, name='registerdealer'),
    path('portal/registeradmin/', views.registeradmin, name='registeradmin'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('shelby/', views.shelby, name='shelby'),
    path('shelby/dealers/', views.dealers, name='dealers'),
    path('shelby/events/', views.events, name='events'),
    path('shelby/shop/', views.shop, name='shop'),
    path('shelby/news/', views.news, name='news'),
    path('shelby/contact/', views.contact, name='contact'),
    path('shelby/vehicle/', views.vehicledesc, name='vehicledesc'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)