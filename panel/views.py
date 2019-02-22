from django.shortcuts import render, redirect, Http404, reverse
from django.views import generic
from digg_paginator import DiggPaginator
from django.conf import settings
from .models import Module
from servers.models import Server
from django.db.models import Q
from jailbreak import models
from api import forms
import requests
import json


class ManagerServerList(generic.ListView):
    context_object_name = 'server_list'
    template_name = 'panel/manager/index.html'

    def dispatch(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('mainpage:home'))
        else:
            return super().dispatch(request, *args, **kwargs) 

    def get_queryset(self):
        if Server.objects.filter(managers=self.request.user).count() == 0:
            manager_exists = False
        else:
            manager_exists = True
            servers = Server.objects.filter(managers=self.request.user)

        if self.request.user.is_superuser is True:
            servers = Server.objects.all()
            user_is_superuser = True
        else:
            user_is_superuser = False

        if manager_exists or user_is_superuser:
            return servers
        else:
            return None   

class ManagerModuleList(generic.ListView):
    context_object_name = 'module_list'
    template_name = 'panel/manager/modules.html'

    def get_queryset(self):
        try:
            server = Server.objects.get(Q(managers=self.request.user) & Q(tag=self.kwargs['server_tag']))
            manager_exists = True
        except Server.DoesNotExist:
            manager_exists = False

        if self.request.user.is_superuser is True:
            server = Server.objects.get(tag=self.kwargs['server_tag'])
            user_is_superuser = True
        else:
            user_is_superuser = False

        if manager_exists or user_is_superuser:
            return Module.objects.filter(servers=server)
        else:
            return None

    def dispatch(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if queryset is None:
            return redirect(reverse('mainpage:home'))
        else:
            return super().dispatch(request, *args, **kwargs)

    def get_server_list(self):
        return Server.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'server_tag': self.kwargs['server_tag'],
            'server_list': self.get_server_list()
        })
        return context


class ManagerModuleDetail(generic.DetailView):
    context_object_name = 'data_with_paginate'
    template_name = 'panel/manager/module/detail.html'

    def get_response_json(self):
        url = '%s/%s/%s' % (settings.API_URL,
                            self.kwargs['server_tag'], self.kwargs['module_tag'])
        return requests.get(url)

    def get_object(self):
        try:
            server = Server.objects.get(Q(managers=self.request.user) & Q(tag=self.kwargs['server_tag']))
            manager_exists = True
        except:
            manager_exists = False

        if self.request.user.is_superuser is True:
            server = Server.objects.get(tag=self.kwargs['server_tag'])
            user_is_superuser = True
        else:
            user_is_superuser = False

        if manager_exists or user_is_superuser:
            row = self.get_response_json()
            if row.status_code == 200:
                data = row.json()
                digg_paginator = DiggPaginator(data, 10)
                page = self.request.GET.get('page')
                return digg_paginator.get_page(page)
            else:
                return None
        else:
            return None

        def dispatch(self, request, *args, **kwargs):
            queryset = self.get_queryset()
            if queryset is None:
                return redirect(reverse('mainpage:home'))
            else:
                return super().dispatch(request, *args, **kwargs)

    def get_module_list(self):
        server = Server.objects.get(tag=self.kwargs['server_tag'])
        return Module.objects.filter(servers=server)

    def get_server_list(self):
        return Server.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        obj = self.get_object()
        context.update({
            'module_tag': self.kwargs['module_tag'],
            'server_tag': self.kwargs['server_tag'],
            'module_list': self.get_module_list(),
            'server_list': self.get_server_list(),
        })
        return context


class ManagerModuleCreate(generic.TemplateView):
    template_name = 'panel/manager/module/create.html'
    
    #*Pobieramy adres api według tagu serwera oraz tagu modułu
    def get_url(self, **kwargs):
        url = '%s/%s/%s' % (
            settings.API_URL,
            self.kwargs['server_tag'], 
            self.kwargs['module_tag']
        )
        return url

    #*Pobieramy liste modułów panelu
    def get_module_list(self):
        server = Server.objects.get(tag=self.kwargs['server_tag'])
        return Module.objects.filter(servers=server)

    #*Pobieramy liste serwerów
    def get_server_list(self):
        return Server.objects.all()

    #*Przkierowujemy użytkownika do strony 
    def redirect_reverse(self, *args):
        kwargs_data = {
            'server_tag': self.kwargs['server_tag'],
            'module_tag': self.kwargs['module_tag']
        }
        return redirect(reverse(args[0], kwargs=kwargs_data))

    #*Wysyłamy dane do API
    def insert_data(self, **kwargs):
        url = self.get_url()
        return requests.post(url, data=kwargs['data'])

    #*Pobieramy grupy administratorów
    def get_admin_groups_response(self):
        url = '%s/%s/admins-groups/' % (
            settings.API_URL,
            self.kwargs['server_tag']
        )
        response = requests.get(url)
        row = response.json()
        row_list = []
        #Wpisujemy do listy na piewrsze miejsce pustę pole
        row_list.insert(0, (None, '------'))
        for i in row:
            row_list.append((i['id'], i['name']))
        return row_list

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context['form']
        if self.kwargs['module_tag'] == 'ccc':
            if form.is_valid():
                data = {
                    "identity": form.cleaned_data['identity'],
                    "tag": form.cleaned_data['tag'],
                    "flag": form.cleaned_data['flag'],
                    "tagcolor": form.cleaned_data['tagcolor'],
                    "namecolor": form.cleaned_data['namecolor'],
                    "textcolor": form.cleaned_data['textcolor'],
                    "alias": form.cleaned_data['alias']
                }
                self.insert_data(data=data)
                return self.redirect_reverse('panel:manager-module')
            else:
                return redirect(reverse('mainpage:home'))
        elif self.kwargs['module_tag'] == 'admins':
            if form.is_valid():
                data = {
                    "authtype": form.cleaned_data['authtype'],
                    "identity": form.cleaned_data['identity'],
                    "password": form.cleaned_data['password'],
                    "flags": form.cleaned_data['flags'],
                    "name": form.cleaned_data['name'],
                    "immunity": form.cleaned_data['immunity'],
                    "group": form.cleaned_data['groups']
                }
                self.insert_data(data=data)
                return self.redirect_reverse('panel:manager-module')
            else:
                return redirect(reverse('mainpage:home'))
        elif self.kwargs['module_tag'] == 'admins-groups':
            if form.is_valid():
                data = {
                    "flags": form.cleaned_data['flags'],
                    "name": form.cleaned_data['name'],
                    "immunity_level": form.cleaned_data['immunity_level']
                }
                self.insert_data(data=data)
                return self.redirect_reverse('panel:manager-module')
            else:
                return redirect(reverse('mainpage:home'))
        return super().render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.kwargs['module_tag'] == 'ccc':
            form = forms.CCCForm(self.request.POST)
        elif self.kwargs['module_tag'] == 'admins-groups':
            form = forms.GroupsForm(self.request.POST)
        elif self.kwargs['module_tag'] == 'admins':
            row_list = self.get_admin_groups_response()
            form = forms.AdminsForm(row_list, self.request.POST)

        context.update({
            'module_tag': self.kwargs['module_tag'],
            'server_tag': self.kwargs['server_tag'],
            'module_list': self.get_module_list(),
            'server_list': self.get_server_list(),
            'form': form
        })
        return context


class ManagerModuleUpdate(generic.TemplateView):
    template_name = 'panel/manager/module/update.html'

    def get_url(self):
        url = '%s/%s/%s/%s' % (
            settings.API_URL,
            self.kwargs['server_tag'], 
            self.kwargs['module_tag'],
            self.kwargs['pk']
        )
        return url

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.kwargs['module_tag'] == 'ccc':
            url = self.get_url()
            response = requests.get(url)
            row = response.json()
            data = {
                'identity': row['identity'],
                'flag': row['flag'],
                'tag': row['tag'],
                'tagcolor': row['tagcolor'],
                'namecolor': row['namecolor'],
                'textcolor': row['textcolor'],
                'alias': row['alias']
            }
            form = forms.CCCForm(self.request.POST)
        elif self.kwargs['module_tag'] == 'admins-groups':
            url = self.get_url()
            response = requests.get(url)
            row = response.json()
            data = {
                'flags': row['flags'],
                'name': row['name'],
                'immunity_level': row['immunity_level'],
            }
            form = forms.GroupsForm(initial=data)

        elif self.kwargs['module_tag'] == 'admins':
            groups_url = '%s/%s/%s'
            url = '%s/%s/admins-groups/' % (
                settings.API_URL,
                self.kwargs['server_tag']
            )
            response = requests.get(groups_url)
            row = response.json()
            row_list = []
            row_list.insert(0, ('', '------'))
            for i in row:
                row_list.append((i['id'], i['name']))

            url = self.get_url()
            response2 = requests.get(url)
            row2 = response2.json()
            data = {
                'authtype': row2['authtype'],
                'identity': row2['identity'],
                'password': row2['password'],
                'flags': row2['flags'],
                'name': row2['name'],
                'immunity': row2['immunity'],
                'groups': row2['groups']
            }
            form = forms.AdminsForm(row_list, initial=data)

        context.update({
            'module_tag': self.kwargs['module_tag'],
            'server_tag': self.kwargs['server_tag'],
            'form': form,
        })
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context['form']
        if self.kwargs['module_tag'] == 'ccc':
            if form.is_valid():
                url = self.get_url()
                data = {
                    'identity': form.cleaned_data['identity'],
                    'flag': form.cleaned_data['flag'],
                    'tag': form.cleaned_data['tag'],
                    'tagcolor': form.cleaned_data['tagcolor'],
                    'namecolor': form.cleaned_data['namecolor'],
                    'textcolor': form.cleaned_data['textcolor'],
                    'alias': form.cleaned_data['alias']
                }
                kwargs = {
                    'server_tag': context['server_tag'],
                    'module_tag': context['module_tag']
                }
                response = requests.put(url, data=data)
                return redirect('/panel/jailbreak/ccc')
        return super(ManagerModuleUpdate, self).render_to_response(context)

class ManagerModuleDelete(generic.TemplateView):
    template_name = 'panel/manager/module/delete.html'

    def get_response_json(self):
        url = '%s/%s/%s/%s' % (
            settings.API_URL,
            self.kwargs['server_tag'], 
            self.kwargs['module_tag'], 
            self.kwargs['pk']
        )
        reponse = requests.get(url)
        return reponse.json()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'module': self.get_response_json(),
            'module_tag': self.kwargs['module_tag'],
            'server_tag': self.kwargs['server_tag']
        })
        return context
