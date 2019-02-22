from django.urls import path
from django.contrib.auth.decorators import permission_required
from django.views.decorators.cache import cache_page
from panel import views

app_name = 'panel'

urlpatterns = [
    path(
        '',
        permission_required('panel.view_module') 
        (
            cache_page(60 * 15)
            (views.ManagerServerList.as_view())
        ), 
        name='manager-index'
    ),
    path(
        '<str:server_tag>/',
        permission_required('panel.view_module') 
        (
            cache_page(60 * 15)
            (views.ManagerModuleList.as_view())
        ), 
        name='manager-server'
    ),
    path(
        '<str:server_tag>/<str:module_tag>/',
        permission_required('panel.view_module') 
        (   
            cache_page(60 * 15)
            (views.ManagerModuleDetail.as_view())
        ), 
        name='manager-module'
    ),
    path(
        '<str:server_tag>/<str:module_tag>/add', 
        views.ManagerModuleCreate.as_view(), 
        name='manager-module-add'
    ),
    path(
        '<str:server_tag>/<str:module_tag>/<int:pk>/edit',
        views.ManagerModuleUpdate.as_view(),
        name='manager-module-update'
    ),
    path(
        '<str:server_tag>/<str:module_tag>/<int:pk>/delete', 
        views.ManagerModuleDelete.as_view(), 
        name='manager-module-delete'
    ),
]