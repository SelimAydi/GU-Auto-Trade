from django.urls import include, path

from . import views
from django.contrib.auth.views import login
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name='index'),
    path('dealerlogin/', login, {'template_name': 'dealerportal/dealerlogin.html'}),
    path('dealerlogin/order/', views.dealerportal, name='dealerportal'),
    path('dealerlogin/upload/', views.upload, name='upload'),
    path('dealerlogin/myorders/', views.myorders, name='myorders'),
    path('dealerlogin/orderlist/', views.orderlist, name='orderlist'),
    path('dealerlogin/registerdealer/', views.registerdealer, name='registerdealer'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('shelby/', views.shelby, name='shelby'),
    path('shelby/contact/', views.contact, name='contact'),
    path('shelby/vehicle/', views.vehicledesc, name='vehicledesc'),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)