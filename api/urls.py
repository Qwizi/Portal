from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'appliaction-comment', views.ApplicationComment)

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('jailbreak/', include('jailbreak.urls')),
    path('api-auth/', include('rest_framework.urls'))
]