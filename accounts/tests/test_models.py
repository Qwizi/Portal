from django.test import TestCase
from accounts import models
import datetime
class AccountsModelsTest(TestCase):
    def test_mygroup_creation(self):
        mygroup = models.MyGroup.objects.create(
            name="Test"
        )
        self.assertTrue(isinstance(mygroup, models.MyGroup))
        self.assertEqual(mygroup.name, "Test")

    def to_steamid32(self, steamid64):
        steamid64ident = 76561197960265728
        steamid = []
        steamid.append('STEAM_0:')
        steamidacct = int(steamid64) - steamid64ident

        if steamidacct % 2 == 0:
            steamid.append('0:')
        else:
            steamid.append('1:')
        steamid.append(str(steamidacct // 2))

        return ''.join(steamid)

    def test_user_creation(self):
        steamid64 = "76561198190469450"
        user = models.User.objects.create(
            username="Test",
            steamid64=steamid64,
            steamid32=self.to_steamid32(steamid64),
            email="test@test.pl",
            date_joined=datetime.datetime.now(),
            is_active=True,
            is_staff=True,
        )

        self.assertTrue(isinstance(user, models.User))
        self.assertEqual(user.steamid32, "STEAM_0:0:115101861")

    def test_paymenthistory_creation(self):
        steamid64 = "76561198190469450"
        user_history = models.User.objects.create(
            username="Test payment history",
            steamid64=steamid64,
            steamid32=self.to_steamid32(steamid64),
            email="test@test.pl",
            date_joined=datetime.datetime.now(),
            is_active=True,
            is_staff=True,
        )
        paymenthistory = models.PaymentHistory.objects.create(
            user=user_history,
            change="-50zł",
            description="Odjecie 50 zł",
            date=datetime.datetime.now(),
            type="SHOP"
        )
        self.assertTrue(isinstance(paymenthistory, models.PaymentHistory))
        self.assertTrue(isinstance(user_history, models.User))
        self.assertEqual(paymenthistory.type, "SHOP")
        self.assertEqual(user_history.username, "Test payment history")
