from django.urls import path
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.cache import cache_page
from . import views

app_name = 'mainpage'

urlpatterns = [
    path('', cache_page(60 * 15) (views.Index.as_view()), name='home'),
    path('login', views.accounts_login, name='login'),
    path('login/process', views.accounts_login_process, name='login-process'),
    path('logout', login_required(views.LogoutUser.as_view()), name='logout'),
    path('rules/', cache_page(60 * 15) (views.RuleList.as_view()), name='rules'),
    path('rules/<int:pk>', views.RuleDetail.as_view(), name='rules-detail'),
    path('rules/add', permission_required('mainpage.add_Rule') (views.RuleCreate.as_view()),  name='rules-add'),
    path('rules/<int:pk>/edit',permission_required('mainpage.change_Rule') (views.RuleUpdate.as_view()), name='rules-update'),
    path('rules/<int:pk>/delete',permission_required('mainpage.delete_Rule')(views.RuleDelete.as_view()), name='rules-delete'),
    path('faq/',cache_page(60 * 15) (views.FAQList.as_view()), name='faq-list'),
]