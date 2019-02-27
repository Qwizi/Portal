from django.test import TestCase, Client
from django.urls import reverse
from accounts import views, models
from shop.models import Bonus, Service, Price
from servers.models import Server

class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username='Test',
            steamid64='76561198190469453',
            steamid32='STEAM_0:0:115104567',
            is_staff=False,
            is_superuser=False
        )

    def test_account_index_annonymous(self):
        response = self.client.get(reverse('accounts:index'))
        self.assertEqual(response.status_code, 302)

    def test_account_index_login(self):
        self.client.login(steamid64=self.user.steamid64)
        response = self.client.get(reverse('accounts:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/index.html')

    def test_wallet_index_annonymous(self):
        response = self.client.get(reverse('accounts:wallet-index'))
        self.assertEqual(response.status_code, 200)

    def test_wallet_index_login(self):
        self.client.login(steamid64=self.user.steamid64)
        response = self.client.get(reverse('accounts:wallet-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/wallet/index.html')

    def test_wallet_payment(self):
        payment = 'sms'
        request = self.factory.get(reverse('accounts:wallet-payment', kwargs={'payment': payment}))
        view = views.WalletPayment.as_view()
        response = view(request, payment=payment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/wallet/payment.html')

    def test_wallet_add(self):
        payment = 'sms'
        request = self.factory.get(reverse('accounts:wallet-add', kwargs={'payment': payment}))
        view = views.WalletAdd.as_view()
        response = view(request, payment=payment)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/wallet/add.html')

    def test_wallet_transfer(self):
        request = self.factory.get(reverse('accounts:wallet-transfer'))
        view = views.WalletTransferMoney.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/wallet/transfer.html')

    def test_wallet_payment_history(self):
        request = self.factory.get(reverse('accounts:wallet-payment-history'))
        view = views.WalletPaymentHistory.as_view()
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/wallet/history.html')

    def test_myshopping(self):
        request = self.factory.get(reverse('accounts:myshopping'))
        view = views.MyShopping.as_view()
        request.user = self.user
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/myshopping.html')