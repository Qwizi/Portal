from django.urls import path
from shop import views
from django.contrib.auth.decorators import permission_required

app_name = 'shop'

urlpatterns = [
    path('', views.ShopIndex.as_view(),name='index'),
    path('<str:service_tag>-<int:service_days>',permission_required('shop.view_bonus')(views.ShopServiceDetail.as_view()),name='service'),
    path('<str:service_tag>-<int:service_days>-<str:server_tag>/finish',permission_required('shop.view_bonus')(views.ShopServiceFinish.as_view()),name='finish'),
    path('admin/',views.ShopList.as_view(),name='list'),
    path('admin/add',views.ShopAdd.as_view(),name='add'),
    path('cron',views.ShopCron.as_view(),name='cron')
]
