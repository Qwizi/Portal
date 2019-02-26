from django.test import TestCase, RequestFactory
from jailbreak import models
import datetime

class JailBreakModelsTest(TestCase):
    def test_storeplayer_creaton(self):
        player = models.StorePlayer.objects.create(
            authid="Test",
            name="Test",
            credits=50,
            date_of_join=datetime.datetime.now(),
            date_of_last_join=datetime.datetime.now()
        )
        self.assertTrue(isinstance(player, models.StorePlayer))
        self.assertEqual(player.credits, 50)

    """     
    def test_storeitem_creation(self):
        player = models.StorePlayer.objects.create(
            authid="Test",
            name="Test",
            credits=50,
            date_of_join=datetime.datetime.now(),
            date_of_last_join=datetime.datetime.now()
        )
        item = models.StoreItem.objects.create(
            player_id = player.id,
            type=,
            unique_id=,
            
        ) 
        """

    def test_customchatcolor_creaton(self):
        ccc = models.CustomChatColor.objects.create(
            alias="Test",
            identity="Test",
            flag="z",
            tag="[Test]",
            tagcolor="#fff",
            namecolor="#fff",
            textcolor="#fff"
        )
        self.assertTrue(isinstance(ccc, models.CustomChatColor))
        self.assertEqual(ccc.tag, "[Test]")

    def test_sourcemodgroup_creation(self):
        group = models.SourceModGroup.objects.create(
            name="Test",
            flags="z",
            immunity_level="100"
        )
        self.assertTrue(isinstance(group, models.SourceModGroup))
        self.assertEqual(group.name, "Test")

    def test_sourcemodadmin_creation(self):
        admin = models.SourceModAdmin.objects.create(
            authtype="STEAM",
            identity="Test",
            flags="z",
            name="Test",
            immunity="100",
        )
        self.assertTrue(isinstance(admin, models.SourceModAdmin))
        self.assertEqual(admin.name, "Test")

    def test_sourcemodadmin_with_groups_creation(self):
        admin_group =  models.SourceModGroup.objects.create(
            flags="z",
            name="Grupa Admina",
            immunity_level="100",
        )
        admin_with_group = models.SourceModAdmin.objects.create(
            authtype="STEAM",
            identity="Grupa Admina",
            flags="z",
            name="Test",
            immunity="100",
        )
        admin_with_group.groups.add(admin_group)
        self.assertTrue(isinstance(admin_group, models.SourceModGroup))
        self.assertTrue(isinstance(admin_with_group, models.SourceModAdmin))
        self.assertEqual(admin_group.name, "Grupa Admina")
        self.assertEqual(admin_with_group.name, "Test")