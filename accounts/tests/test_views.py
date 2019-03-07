from django.test import TestCase, Client
from django.urls import reverse
from accounts import views, models
from shop.models import Bonus, Service, Price
from servers.models import Server
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission

class AccountsViewsTestCase(TestCase):
    def setUp(self):
        self.user = models.User.objects.create(
            username='Test',
            steamid64='76561198190469453',
            steamid32='STEAM_0:0:115104567',
            is_staff=False,
            is_superuser=False
        )
        usergroup = models.MyGroup.objects.create(pk=2, name="Użytkownik")

        accounts_ct = ContentType.objects.get(app_label='accounts', model='User')

        perms_list = [
            'view_account',
            'view_wallet',
            'add_wallet',
            'transfer_wallet'
        ]
        for perm in perms_list:
            account_perm = Permission.objects.get(codename=perm, content_type=accounts_ct)
            usergroup.permissions.add(account_perm)

        usergroup.user_set.add(self.user)

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
        self.assertEqual(response.status_code, 302)

    def test_wallet_index_login(self):
        self.client.login(steamid64=self.user.steamid64)
        response = self.client.get(reverse('accounts:wallet-index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/wallet/index.html')