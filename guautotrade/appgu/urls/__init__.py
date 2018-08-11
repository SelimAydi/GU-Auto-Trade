from django.urls import include
from ..views import base_index
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings

from .api import *
from .shelby import *

urlpatterns = [
    path('', base_index.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('portal/', include('appgu.urls.portal')),
    # path('', include('appgu.urls.guautotrade')),
    path('shelby/', include('appgu.urls.shelby')),
    path('tuscany/', include('appgu.urls.tuscany')),
    path('api/', include('appgu.urls.api')),
]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)