from django.urls import path
from accounts import views
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'accounts'

urlpatterns = [
    path('', permission_required('accounts.view_account')(views.AccountIndex.as_view()), name='index'),
    path('wallet/', permission_required('accounts.view_wallet')(views.WalletIndex.as_view()), name='wallet-index'),
    path('wallet/payment/<str:payment>', permission_required('accounts.add_wallet')(views.WalletPayment.as_view()), name='wallet-payment'),
    path('wallet/payment/<str:payment>/add', permission_required('accounts.add_wallet')(views.WalletAdd.as_view()), name='wallet-add'),
    path('wallet/payment/<str:payment>/success', views.WalletSuccess.as_view(), name='wallet-success'),
    path('wallet/transfer', permission_required('accounts.transfer_wallet')(views.WalletTransferMoney.as_view()), name='wallet-transfer'),
    path('wallet/historia',permission_required('accounts.view_wallet')(views.WalletPaymentHistory.as_view()),name='wallet-payment-history'),
    path('my-shopping', permission_required('accounts.view_myshopping')(views.MyShopping.as_view()), name='myshopping'),
]