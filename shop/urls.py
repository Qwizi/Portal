from django.urls import path
from .views import Index, ServiceDetail, ServiceFinish, ShopAdd, ShopList, Cron
from django.contrib.auth.decorators import permission_required

app_name = 'shop'

urlpatterns = [
    path(
        '',
        permission_required('shop.view_bonus')
        (Index.as_view()),
        name='index'
    ),
    path(
        '<str:service_tag>-<int:service_days>',
        permission_required('shop.view_bonus')
        (ServiceDetail.as_view()),
        name='service'
    ),
    path(
        '<str:service_tag>-<int:service_days>-<str:server_tag>/finish',
        permission_required('shop.view_bonus')
        (ServiceFinish.as_view()),
        name='finish'
    ),
    path(
        'admin/',
        ShopList.as_view(),
        name='list'
    ),
    path(
        'admin/add',
        ShopAdd.as_view(),
        name='add'
    ),
    path(
        'cron',
        Cron.as_view(),
        name='cron'
    )
]
