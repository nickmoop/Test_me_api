from django.conf.urls import url

from django.conf import settings
from django.conf.urls.static import static

from test_me_api import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^api/(?P<api_command>\w+)', views.apiProcessor),
    url(r'^uploadTextPage', views.uploadTextPage),
    url(r'^admin', views.admin),
]
