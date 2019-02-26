from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'sourcebans'

urlpatterns = [
    path('', views.BansIndex.as_view(), name='index')
]