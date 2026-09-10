from django.conf.urls import url
from .views import ajax_reset_form


urlpatterns = [
    url(r'^reset_form/$', ajax_reset_form, name='ajax_reset_form')
]
