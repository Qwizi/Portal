from django.urls import path
from . import views

urlpatterns = [
    path('', views.servers_list, name="servers_list"),
]