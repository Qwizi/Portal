from django.urls import path
from . import views
from django.contrib.auth.decorators import permission_required, login_required

app_name = 'user_centrum'

urlpatterns = [
    path(
        '',
        login_required() 
        (views.Index.as_view()),
        name='index'
    ),
    path(
        'applications/',
        permission_required('user_centrum.view_application')
        (views.ApplicationList.as_view()),
        name='application-list'
    ),
    path(
        'applications/<int:pk>',
        permission_required('user_centrum.view_application')
        (views.ApplicationDetail.as_view()),
        name='application-detail'
    ),
    path(
        'applications/add',
        permission_required('user_centrum.add_application')
        (views.ApplicationCreate.as_view()),
        name='application-create'
    ),
    path(
        'applications/<int:pk>/edit',
        permission_required('user_centrum.change_application')
        (views.ApplicationUpdate.as_view()),
        name='application-update'
    ),
    path(
        'applications/<int:pk>/delete',
        permission_required('user_centrum.delete_application')
        (views.ApplicationDelete.as_view()),
        name='application-delete'
    ),
    path(
        'applications/<int:pk>/accept',
        permission_required('user_centrum.accept_application')
        (views.ApplicationAccept.as_view()),
        name='application-accept'
    ),
    path(
        'applications/<int:pk>/cancel',
        permission_required('user_centrum.cancel_application')
        (views.ApplicationCancel.as_view()),
        name='application-cancel'
    ),
    path(
        'applications/<int:pk>/com/<int:comment_pk>/delete',
        permission_required('user_centrum.delete_applicationcomments')
        (views.ApplicationCommentsDelete.as_view()),
        name='application-comments-delete'
    ),
    path(
        'applications/<int:pk>/com/<int:comment_pk>/edit',
        permission_required('user_centrum.delete_applicationcomments')
        (views.ApplicationCommentsUpdate.as_view()),
        name='application-comments-update'
    ),
]