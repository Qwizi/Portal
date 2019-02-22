from django.test import TestCase, RequestFactory
from django.urls import reverse
from jailbreak import models, views


class JailBreakViewsTest(TestCase):

    def setUp(self):
        self.fk = RequestFactory()

    def test_ccc_list(self):
        request = self.fk.get('/api/jailbreak/ccc/')
        view = views.CCCList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)