# # from django.contrib.auth import views
# from django.urls import include
# from ..views import base_index
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf.urls.static import static
# from django.conf import settings
# from .. import lel
# # from ..testing import getLogin
# # from django.contrib.auth.views import login
# # # import django.contrib.auth.views
# #
from .api import *
from .shelby import *
from .portal import *
#
# urlpatterns = [
#     path('', base_index.index, name='index'),
#     path('accounts/', include('django.contrib.auth.urls')),
#     # path('portal/', getLogin(), {'template_name': 'portal/index.html'}),
#     path('portal/', include('appgu.urls.portal')),
#     # path('', include('appgu.urls.guautotrade')),
#     path('shelby/', include('appgu.urls.shelby')),
#     path('tuscany/', include('appgu.urls.tuscany')),
#     path('api/', include('appgu.urls.api')),
#     path('lel/', lel, name='lel'),
# ]
#
# urlpatterns += staticfiles_urlpatterns()
# urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)