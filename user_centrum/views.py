from django.shortcuts import reverse
from django.db.models import Q
from django.views import generic
from django.conf import settings

from .models import Application, ApplicationComments
from .forms import (
    ApplicationModelForm,
    ApplicationModelFormCreate,
    ApplicationCommentsModelFormCreate)
from sourcebans.models import Ban, Comm

from digg_paginator import DiggPaginator
import requests
# Lista dostępnych skrotow


class Index(generic.TemplateView):
    template_name = 'user_centrum/index.html'

# Lista podan


class ApplicationList(generic.ListView):
    context_object_name = 'data_with_paginate'
    template_name = 'user_centrum/application/list.html'

    def get_queryset(self):
        digg_paginator = DiggPaginator(
            Application.objects.all().order_by('-pk'), 10)
        page = self.request.GET.get('page')
        return digg_paginator.get_page(page)

# Detale podania


class ApplicationDetail(generic.DetailView):
    model = Application
    context_object_name = 'application'
    template_name = 'user_centrum/application/detail.html'

    # Pobiernie liczby otrzymanych banów
    def get_count_bans(self):
        obj = self.get_object()
        bans = Ban.objects.filter(
            Q(authid=obj.owner.steamid32) & Q(sid=obj.server)
        ).count()
        return bans

    # Pobieranie liczby otrzymanych blokad komunikacji
    def get_count_comms(self):
        obj = self.get_object()
        comms = Comm.objects.filter(
            Q(authid=obj.owner.steamid32) & Q(sid=obj.server)).count()
        return comms

    # Tworzenie paginacji
    def make_paggination(self, queryset, limit):
        digg_paginator = DiggPaginator(queryset, limit)
        page = self.request.GET.get('page')
        return digg_paginator.get_page(page)

    # Sprawdzanie czy rekrut posiada blokadę vac
    def check_vac(self):
        obj = self.get_object()
        base_url = 'https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/'
        data = {
            'key': settings.STEAM_API_KEY,
            'steamids': obj.owner.steamid64
        }
        r = requests.get(base_url, params=data)
        raw_data = r.json()
        vac = raw_data['players'][0]['VACBanned']
        return vac

    # Pobieranie komentarzty do podania
    def get_comments(self):
        obj = self.get_object()
        comments = ApplicationComments.objects.filter(
            application=obj).order_by('-pk')
        return comments

    def get_context_data(self, **kwargs):
        context = super(ApplicationDetail, self).get_context_data(**kwargs)
        obj = self.get_object()

        bans = self.get_count_bans()
        comms = self.get_count_comms()
        comments = self.get_comments()
        vac = self.check_vac()

        form = ApplicationCommentsModelFormCreate(initial={
            'application': obj,
            'owner': self.request.user,
            'owner_name': self.request.user.username,
            'owner_avatar': self.request.user.avatar_medium,
            'count_com': comments.count
        })

        context.update({
            'bans': bans,
            'cbans': comms,
            'vac': vac,
            'comments': comments,
            'data_with_paginate': self.make_paggination(comments, 15),
            'form': form
        })
        return context

    # Odbieranie rządań POST i wysyłanie na endpoint api. Tworzenie komentarza
    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        data = {
            "content": self.request.POST.get('content'),
            "application": self.request.POST.get('application'),
            "owner": self.request.POST.get('owner')
        }
        requests.post(
            'http://localhost:8000/api/applications-comments/', data=data)
        return self.render_to_response(context=context)

# Tworzenie podania


class ApplicationCreate(generic.CreateView):
    model = Application
    form_class = ApplicationModelFormCreate
    template_name = 'user_centrum/application/create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.owner = self.request.user
        return super(ApplicationCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('centrum:application-detail', kwargs={'pk': self.object.pk})

# Edycja podania


class ApplicationUpdate(generic.UpdateView):
    model = Application
    form_class = ApplicationModelForm
    template_name = 'user_centrum/application/update.html'

    def get_success_url(self):
        return reverse('centrum:application-detail', kwargs={'pk': self.kwargs['pk']})

# Usuwanie podania


class ApplicationDelete(generic.DeleteView):
    model = Application
    form_class = ApplicationModelForm
    template_name = 'user_centrum/application/delete.html'

    def get_success_url(self):
        return reverse('centrum:application-list')

# Akceptowanie podan


class ApplicationAccept(generic.RedirectView):
    """
    Akceptowanie podania
    """

    def get(self, request, *args, **kwargs):
        app = Application.objects.get(pk=self.kwargs['pk'])
        app.accept()
        self.url = reverse('centrum:application-detail', kwargs={'pk': app.pk})
        return super(ApplicationAccept, self).get(request, *args, **kwargs)

# Odrzucanie podania


class ApplicationCancel(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        app = Application.objects.get(pk=self.kwargs['pk'])
        app.cancel()
        self.url = reverse('centrum:application-detail', kwargs={'pk': app.pk})
        return super(ApplicationCancel, self).get(request, *args, **kwargs)

# Usuwanie komentarza


class ApplicationCommentsDelete(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        data = {
            'id': self.kwargs['comment_pk']
        }
        requests.delete(
            'http://localhost:8000/api/applications-comments/%d' % (
                self.kwargs['comment_pk']),
            data=data
        )
        self.url = reverse('centrum:application-detail',
                           kwargs={'pk': self.kwargs['pk']})
        return super(ApplicationCommentsDelete, self).get(request, *args, **kwargs)

# Aktualizowanie komentarza


class ApplicationCommentsUpdate(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        data = {
            'id': self.kwargs['comment_pk']
        }
        requests.put('http://localhost:8000/api/applications-comments/%d' %
                     (self.kwargs['comment_pk']), data=data)
        self.url = reverse('centrum:application-detail',
                           kwargs={'pk': self.kwargs['pk']})
        return super(ApplicationCommentsUpdate, self).get(request, *args, **kwargs)
