from django.test import TestCase, RequestFactory
from django.urls import reverse
from accounts import views, models
from shop.models import Bonus, Service, Price
from servers.models import Server

class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username='Test',
            steamid64='76561198190469450',
            steamid32='STEAM_0:0:115101861',
            is_staff=True,
            is_superuser=True
        )
        self.server = Server.objects.create(
            name='Test',
            ip='XXXX.XXXX.XXXX.XXXX',
            port='XXXX',
            tag='test'
        )
        self.bonus = Bonus.objects.create(
            name='Test',
            tag='test',
            flags='t',
            description='test',
            description_full='test_full',
        )
        self.bonus.servers.add(self.server)
        self.price = Price.objects.create(value='5.00')
        self.service = Service.objects.create(
            price=self.price,
            days=7,
            bonus=self.bonus
        )
        self.factory = RequestFactory()

    def test_index(self):
        request = self.factory.get(reverse('accounts:index'))
        view = views.Index.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'accounts/index.html')

    def test_wallet_index(self):
        request = self.factory.get(reverse('accounts:wallet-index'))
        view = views.WalletIndex.as_view(template_name='accounts/wallet/index.html')
        response = view(request)
        self.assertEqual(response.status_code, 200)

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