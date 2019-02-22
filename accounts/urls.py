from django.urls import path
from accounts.views import Index, WalletIndex, WalletPayment, WalletAdd, WalletSuccess, MyShopping, WalletTransferMoney, WalletPaymentHistory
from django.contrib.auth.decorators import login_required, permission_required

app_name = 'accounts'

urlpatterns = [
    path(
        '', 
        permission_required('accounts.view_account')
        (Index.as_view()), 
        name='index'
    ),
    path(
        'wallet/', 
        permission_required('accounts.view_wallet')
        (WalletIndex.as_view()), 
        name='wallet-index'
    ),
    path(
        'wallet/payment/<str:payment>', 
        permission_required('accounts.add_wallet')
        (WalletPayment.as_view()), 
        name='wallet-payment'
    ),
    path(
        'wallet/payment/<str:payment>/add', 
        permission_required('accounts.add_wallet')
        (WalletAdd.as_view()), 
        name='wallet-add'
    ),
    path(
        'wallet/payment/<str:payment>/success', 
        WalletSuccess.as_view(), 
        name='wallet-success'
    ),
    path(
        'wallet/transfer', 
        permission_required('accounts.transfer_wallet')
        (WalletTransferMoney.as_view()), 
        name='wallet-transfer'
    ),
    path(
        'wallet/historia',
        permission_required('accounts.view_wallet')
        (WalletPaymentHistory.as_view()),
        name='wallet-payment-history'
    ),
    path(
        'my-shopping', 
        permission_required('accounts.view_myshopping')
        (MyShopping.as_view()), 
        name='myshopping'
    ),
]