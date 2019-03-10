import datetime
import time
from decimal import *

from django.views import generic
from django.db.models import Q
from django.shortcuts import redirect, reverse
from django.contrib import messages
from django.http import HttpResponse

from digg_paginator import DiggPaginator
from servers.models import Server
from accounts.models import PaymentHistory, MyGroup, User
from .forms import ShopForm, ShopAddForm
from .models import Service, Premium, PremiumCache, Bonus, PromotionServicePrice
# Lista usług


class Index(generic.ListView):
    queryset = Service.objects.all()
    context_object_name = 'data_with_paginate'
    template_name = 'shop/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        digg_paginator = DiggPaginator(self.queryset, 10)
        page = self.request.GET.get('page')
        context.update({
            'data_with_paginate': digg_paginator.get_page(page)
        })
        return context

# Lista serwerów na których można zakupić uslugę


class ServiceDetail(generic.DetailView):
    context_object_name = 'service'
    template_name = 'shop/service.html'

    def get_object(self):
        return Service.objects.get(
            Q(bonus__tag=self.kwargs['service_tag'])
            & Q(days=self.kwargs['service_days'])
        )

# Finalizacja zakupu


class ServiceFinish(generic.TemplateView):
    template_name = 'shop/finish.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        server_id = Server.objects.get(pk=self.request.POST.get('server'))
        service_id = Service.objects.get(pk=self.request.POST.get('service'))

        p_nick = self.request.POST.get('nick')
        p_flags = self.request.POST.get('flags')
        p_days = int(self.request.POST.get('days'))
        days_add = datetime.datetime.now() + datetime.timedelta(days=p_days)
        user = self.request.user
        if service_id.promotion_price != 0.0:
            price = service_id.promotion_price
        else:
            price = service_id.price.value

        try:
            premium_cache = PremiumCache.objects.get(
                Q(nick=p_nick) & Q(flags=p_flags)
                & Q(server=server_id) & Q(time__gte=datetime.datetime.now())
            )
            premium_exists = True
        except PremiumCache.DoesNotExist:
            premium_exists = False

        if premium_exists:
            if user.cash >= price:
                premium_cache.time += datetime.timedelta(days=p_days)
                premium_cache.service.days += p_days
                premium_cache.save()
                user.remove_cash(price)
                PaymentHistory.objects.create(
                    user=user,
                    target=user,
                    change="-%.2f zł" % (price),
                    description="Przedłużenie usługi %s o %s dni na serwerze %s" % (
                        service_id.bonus.name, price, server_id.name),
                    type='Sklep'
                )
                SharkGroup = MyGroup.objects.get(pk=6)

                if user.display_group.pk != 6 and user.display_group.pk == 2:
                    user.display_group = SharkGroup
                    user.save()
                
                messages.success(
                    self.request, "Pomyślnie przedłużono usługę %s" % (service_id.bonus.name))
                return redirect(reverse('accounts:myshopping'))
            else:
                messages.error(
                    self.request, "Nie masz środków do zakupu tej usługi. Doładuj portfel.")
                return redirect(reverse('accounts:wallet-index'))
        else:
            if user.cash >= price:
                premium = Premium.objects.create(
                    nick=p_nick,
                    server=server_id,
                    flags=p_flags
                )

                premium_cache = PremiumCache.objects.create(
                    nick=premium.nick,
                    flags=premium.flags,
                    server=premium.server,
                    time=days_add,
                    # user=user
                    premium=premium,
                    service=service_id
                )
                user.remove_cash(price)

                SharkGroup = MyGroup.objects.get(pk=6)

                if user.display_group.pk != 6 and user.display_group.pk == 2:
                    user.display_group = SharkGroup
                    user.save()

                PaymentHistory.objects.create(
                    user=user,
                    target=user,
                    change="-%.2f zł" % (price),
                    description="Zakup usługi %s za %.2f zł" % (
                        service_id.bonus.name, price),
                    type='Sklep'
                )
                messages.success(
                    self.request, "Pomyślnie zakupiono usługę %s" % (service_id.bonus.name))
                return redirect(reverse('accounts:myshopping'))
            else:
                messages.error(
                    self.request, "Nie masz środków do zakupu tej usługi. Doładuj portfel.")
                return redirect(reverse('accounts:wallet-index'))
        return self.render_to_response(context=context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        service = Service.objects.get(
            Q(bonus__tag=self.kwargs['service_tag']) & Q(days=self.kwargs['service_days']))
        server = Server.objects.get(tag=self.kwargs['server_tag'])

        form = ShopForm(initial={
            'nick': self.request.user.steamid32,
            'server': server.pk,
            'service': service.pk,
            'days': service.days,
            'flags': service.bonus.flags,
        })
        context.update({
            'service': service,
            'server': server,
            'server_tag': server.tag,
            'form': form,
        })
        return context

# Zadanie cron usuwające przedawnione usługi


class Cron(generic.View):
    def get(self, request, *args, **kwargs):
        try:
            p_cache = PremiumCache.objects.filter(
                Q(time__lte=datetime.datetime.now()) & Q(premium__isnull=False)
            )
            for i in p_cache:
                i.premium.delete()
                UserGroup = MyGroup.objects.get(pk=2)
                user = User.objects.get(steamid32=i.nick)
                user.display_group = UserGroup
                user.save()
        except PremiumCache.DoesNotExist:
            return HttpResponse('')
        return HttpResponse('')

# lista z zakupionymi usługami


class ShopList(generic.ListView):
    #queryset = PremiumCache.objects.all().order_by('-pk')
    context_object_name = 'data_with_paginate'
    template_name = 'shop/admin/list.html'

    def get_queryset(self):
        digg_paginator = DiggPaginator(
            PremiumCache.objects.all().order_by('-pk'), 15
        )
        page = self.request.GET.get('page')
        return digg_paginator.get_page(page)

# Dodawanie uslug przez admina


class ShopAdd(generic.FormView):
    form_class = ShopAddForm
    template_name = 'shop/admin/create.html'

    def form_valid(self, form):
        p_nick = form.cleaned_data['nick']
        p_server = form.cleaned_data['server']
        p_bonus = form.cleaned_data['bonus']
        p_days = form.cleaned_data['days']
        flags = p_bonus.flags
        days_add = datetime.datetime.now() + datetime.timedelta(days=p_days)

        try:
            Service.objects.get(
                Q(days=p_days) & Q(bonus__pk=p_bonus.pk)
            )
            service_exists = True
        except Service.DoesNotExist:
            service_exists = False

        try:
            bonus = Bonus.objects.get(Q(servers=p_server) & Q(flags=flags))
            bonus_exists = True
        except Bonus.DoesNotExist:
            bonus_exists = False

        if service_exists and bonus_exists:
            service = Service.objects.get(
                Q(days=p_days) & Q(bonus__pk=bonus.pk)
            )

            try:
                premium_cache = PremiumCache.objects.get(
                    Q(nick=p_nick) & Q(flags=bonus.flags) & Q(
                        server=p_server)
                    & Q(time__gte=datetime.datetime.now()
                        )
                )
                premium_exists = True
            except PremiumCache.DoesNotExist:
                premium_exists = False

            if premium_exists:
                premium_cache.time += datetime.timedelta(days=p_days)
                premium_cache.service.days += p_days
                premium_cache.save()
            else:
                premium = Premium.objects.create(
                    nick=p_nick,
                    server=p_server,
                    flags=flags
                )

                PremiumCache.objects.create(
                    nick=premium.nick,
                    server=premium.server,
                    flags=premium.flags,
                    time=days_add,
                    premium=premium,
                    service=service
                )

        return super(ShopAdd, self).form_valid(form)

    def get_success_url(self):
        return reverse('shop:create')
