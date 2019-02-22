from django.shortcuts import get_object_or_404, redirect, reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin

from servers.models import Server
from .models import Rule, FAQ
from sourcebans.models import Bans
from accounts.models import User
from shop.models import Service
from steamauth import RedirectToSteamSignIn, GetSteamID64
from django.shortcuts import render_to_response
from django.template import RequestContext


# 404
def handler404(request, exception, template_name='404.html'):
    response = render_to_response("404.html")
    response.status_code = 404
    return response


# Początek logowania użytkownika
def accounts_login(request):
    return RedirectToSteamSignIn(reverse('mainpage:login-process'), useSSL=False)


# Końcowy proces logowania użytkownika
def accounts_login_process(request):
    # Pobieranie steamid 64
    steamid = GetSteamID64(request.GET)
    if steamid is False:
        return redirect('/login_failed')
    else:
        # *Logowanie zakończyło się sukcesem

        # Autoryzujemy użytkownika
        user = authenticate(request, steamid64=steamid)

        if user is not None:
            # logujemy użytkownika
            login(request, user)
            return redirect(reverse('mainpage:home'))


# Wylogowywanie użytkownika
class LogoutUser(generic.RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)


# Pobieranie banów, serwerów, oraz postów
class Index(generic.ListView):
    model = Server
    context_object_name = 'server_list'
    template_name = 'mainpage/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['ban_list'] = Bans.objects.order_by('-created')
        context['bonus_list'] = Service.objects.all()[:3]
        return context

#Lista regulaminów
class RuleList(generic.ListView):
    model = Rule
    context_object_name = 'rule_list'
    template_name = 'mainpage/rules/list.html'
    queryset = Rule.objects.filter(is_active=True)

#Detale pojedynczego regulaminu
class RuleDetail(generic.DetailView):
    model = Rule
    context_object_name = 'rule'
    template_name = 'mainpage/rules/detail.html'

#Tworzenie nowego regulaminu
class RuleCreate(SuccessMessageMixin, generic.CreateView):
    model = Rule
    fields = ['server', 'content']
    template_name = 'mainpage/rules/create_form.html'
    success_message = 'Pomyślne dodano regulamin'
    success_url = '/regulaminy'

#Edytowanie istniejącego regulaminu
class RuleUpdate(SuccessMessageMixin, generic.UpdateView):
    model = Rule
    fields = ['server', 'content', 'is_active']
    template_name = 'mainpage/rules/update_form.html'
    success_message = 'Pomyślnie edytowano regulamin'

#Usuwanie regulaminu
class RuleDelete(SuccessMessageMixin, generic.DeleteView):
    model = Rule
    success_url = '/regulaminy'
    template_name = 'mainpage/rules/confirm_delete.html'
    success_message = 'Pomyślnie usunieto regulamin'

class FAQList(generic.ListView):
    model = FAQ
    context_object_name = 'FAQ_list'
    template_name = 'mainpage/FAQ/index.html'