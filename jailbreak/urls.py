from django.urls import path, include
from rest_framework import routers
from jailbreak import views

router = routers.DefaultRouter()
router.register(r'ccc', views.CustomChatColorViewSet)


urlpatterns = [
    path('', include(router.urls)),
]