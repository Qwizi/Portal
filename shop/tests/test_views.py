from django.test import TestCase, RequestFactory
from django.urls import reverse
from shop import views, models
from servers.models import Server
from accounts.models import User

class ShopViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(
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
        self.bonus = models.Bonus.objects.create(
            name='Test',
            tag='test',
            flags='t',
            description='test',
            description_full='test_full',
        )
        self.bonus.servers.add(self.server)
        self.price = models.Price.objects.create(value='5.00')
        self.service = models.Service.objects.create(
            price=self.price,
            days=7,
            bonus=self.bonus
        )
        self.fk = RequestFactory()

    def test_index(self):
        request = self.fk.get(reverse('shop:index'))
        view = views.Index.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shop/index.html')

    def test_service_detail(self):
        service_tag = self.service.bonus.tag
        service_days = self.service.days
        request = self.fk.get(reverse('shop:service', kwargs={'service_tag': service_tag, 'service_days': service_days}))
        view = views.ServiceDetail.as_view()
        response = view(request, service_tag=service_tag, service_days=service_days)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shop/service.html')

    def test_service_finish(self):
        service_tag = self.service.bonus.tag
        service_days = self.service.days
        server_tag = self.server.tag
        request = self.fk.get(reverse('shop:finish', kwargs={'service_tag': service_tag, 'service_days': service_days, 'server_tag': server_tag}))
        request.user = self.user
        view = views.ServiceFinish.as_view()
        response = view(request, service_tag=service_tag, service_days=service_days, server_tag=server_tag)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shop/finish.html')

    def test_shop_list(self):
        request = self.fk.get(reverse('shop:list'))
        view = views.ShopList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shop/admin/list.html')

    def test_shop_add(self):
        request = self.fk.get(reverse('shop:add'))
        view = views.ShopAdd.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'shop/admin/create.html')
