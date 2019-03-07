from django.urls import path
from profiles import views

app_name = 'profiles'

urlpatterns = [
    path('<int:pk>', views.ProfileIndex.as_view(), name='index')
]