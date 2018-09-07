from django.contrib import admin
from django.urls import include, path
# from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
# from oscar.app import application

from paypal.express.dashboard.app import application

from appgu.views import base_index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
# import django.contrib.auth.views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('i18n/', include('django.conf.urls.i18n')),
    path('admin/', admin.site.urls),
    path('', base_index.index, name='index'),
    path('checkout/paypal/', include('paypal.express.urls')),
    # Optional
    # path('dashboard/paypal/express/', application.urls),
    path('mollie/', include(('mollie_oscar.urls', 'mollie_oscar'), namespace='mollie_oscar')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('portal/', include('appgu.urls.portal')),
    path('shelby/', include('appgu.urls.shelby')),
    path('tuscany/', include('appgu.urls.tuscany')),
    path('gu/', include('appgu.urls.gu')),
    path('api/', include('appgu.urls.api'))
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)