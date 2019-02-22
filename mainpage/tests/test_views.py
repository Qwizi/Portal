from django.test import TestCase, Client
from django.urls import reverse
from mainpage.models import Rules
from servers.models import Server
from django.test import RequestFactory
from mainpage import views


class MainPageViewsTestCase(TestCase):

    def setUp(self):
        self.server = Server.objects.create(
            name="Test",
            banner="",
            ip="xxx.xxx.xxx",
            port="xxx",
            tag="test"
        )
        self.rule = Rules.objects.create(
            server=self.server,
            content='Test'
        )
        self.client = Client()
        self.factory = RequestFactory()

    def test_home(self):
        request = self.factory.get(reverse('mainpage:home'))
        view = views.Index.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/index.html')

    def test_rules_list(self):
        request = self.factory.get(reverse('mainpage:rules'))
        view = views.RulesList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/rules/list.html')

    def test_rules_detail(self):
        request = self.factory.get(reverse('mainpage:rules-detail', kwargs={'pk': self.rule.pk}))
        view = views.RulesDetail.as_view()
        response = view(request, pk=self.rule.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/rules/detail.html')
    
    def test_rules_add(self):
        request = self.factory.get(reverse('mainpage:rules-add'))
        view = views.RulesCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/rules/create_form.html')

    def test_rules_update(self):
        request = self.factory.get(reverse('mainpage:rules-update', kwargs={'pk': self.rule.pk}))
        view = views.RulesUpdate.as_view()
        response = view(request, pk=self.rule.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/rules/update_form.html')

    def test_rules_delete(self):
        request = self.factory.get(reverse('mainpage:rules-delete', kwargs={'pk': self.rule.pk}))
        view = views.RulesDelete.as_view()
        response = view(request, pk=self.rule.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/rules/confirm_delete.html')

    def test_faq_list(self):
        request = self.factory.get(reverse('mainpage:faq-list'))
        view = views.FaqList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'mainpage/faq/index.html')