from django.test import TestCase, RequestFactory
from django.urls import reverse
from jailbreak import models, views


class JailBreakViewsTest(TestCase):

    def setUp(self):
        self.fk = RequestFactory()

    def test_customchatcolor_viewset(self):
        request = self.fk.get('/api/jailbreak/ccc/')
        view = views.CustomChatColorViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_storeplayer_viewset(self):
        request = self.fk.get('/api/jailbreak/store-players')
        view = views.StorePlayerViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_storeitem_viewset(self):
        request = self.fk.get('/api/jailbreak/store-items')
        view = views.StoreItemViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def store_equipment_viewset(self):
        request = self.fk.get('/api/jailbreak/store-equipment')
        view = views.StoreEquipmentViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_sourcemodadmin_viewset(self):
        request = self.fk.get('/api/jailbreak/admins')
        view = views.SourceModAdminViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)

    def test_sourcemodgroup_viewset(self):
        request = self.fk.get('/api/jailbreak/admins-groups')
        view = views.SourceModGroupViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, 200)
