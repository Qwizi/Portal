from django.test import TestCase, RequestFactory
from django.urls import reverse
from user_centrum import views, models
from accounts.models import User, MyGroup
from servers.models import Server
class UserCentrumViewsTest(TestCase):
    
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
        self.application = models.Application.objects.create(
            owner=self.user,
            type='Admin',
            server=self.server,
            name='Test',
            age='16',
            microphone=True,
            reason='Testowy powod',
            experiance='Testowe doswaidzcenie'
        )
        self.fk = RequestFactory()

    def test_index(self):
        request = self.fk.get(reverse('user_centrum:index'))
        view = views.Index.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_centrum/index.html')

    def test_application_list(self):
        request = self.fk.get(reverse('user_centrum:application-list'))
        view = views.ApplicationList.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_centrum/application/list.html')
    
    def test_application_detail(self):
        request = self.fk.get(reverse('user_centrum:application-detail', kwargs={'pk': self.application.pk}))
        request.user = self.user
        view = views.ApplicationDetail.as_view()
        response = view(request, pk=self.application.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_centrum/application/detail.html')

    def test_application_create(self):
        request = self.fk.get(reverse('user_centrum:application-create'))
        view = views.ApplicationCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_centrum/application/create.html')
    
    def test_application_update(self):
        request = self.fk.get(reverse('user_centrum:application-update', kwargs={'pk': self.application.pk}))
        view = views.ApplicationUpdate.as_view()
        response = view(request, pk=self.application.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_centrum/application/update.html')

    def test_application_delete(self):
        request = self.fk.get(reverse('user_centrum:application-delete', kwargs={'pk': self.application.pk}))
        view = views.ApplicationDelete.as_view()
        response = view(request, pk=self.application.pk)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name[0], 'user_centrum/application/delete.html')

    def test_application_accept(self):
        request = self.fk.get(reverse('user_centrum:application-accept', kwargs={'pk': self.application.pk}))
        view = views.ApplicationAccept.as_view()
        response = view(request, pk=self.application.pk)
        self.assertEqual(response.status_code, 302)

    def test_application_cancel(self):
        request = self.fk.get(reverse('user_centrum:application-cancel', kwargs={'pk': self.application.pk}))
        view = views.ApplicationCancel.as_view()
        response = view(request, pk=self.application.pk)
        self.assertEqual(response.status_code, 302)