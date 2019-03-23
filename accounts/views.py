from django.shortcuts import redirect, reverse, get_object_or_404
from django.conf import settings
from django.views import generic
from django.views.generic.edit import FormMixin
from django.contrib import messages
from django.http import Http404

from shop.models import *
from accounts.models import User, PaymentHistory
from .forms import WalletTransfer, SMSNumberForm, PromotionCodeForm, ReturnCodeForm
from digg_paginator import DiggPaginator
import requests
import urllib.parse
from decimal import *

# Strona głowna panelu użytkownika
class AccountIndex(generic.TemplateView):
    template_name = 'accounts/index.html'

# Strona głowna portfela
class WalletIndex(generic.TemplateView):
    template_name = 'accounts/wallet/index.html'

    def get_payment_list(self):
        return Payment.objects.order_by('-is_active')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'payment_list': self.get_payment_list(),
        })
        return context

# Wybieranie wartości doładowania portfela przez smsa
""" 
class WalletPayment(generic.ListView):
    model = SMSNumber
    context_object_name = 'price_list'
    template_name = 'accounts/wallet/payment.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'payment': self.kwargs['payment'],
            'form': SMSNumberForm(self.request.POST)
        })
        return context 
"""
class WalletPayment(generic.TemplateView):
    template_name = 'accounts/wallet/payment.html'


    def get_payment_form(self):
        form = None
        if self.kwargs['payment'] == 'sms':
            form = SMSNumberForm()
        elif self.kwargs['payment'] == 'promotion_code':
            form = PromotionCodeForm()
        else:
            form = None

        if form is None:
            raise Http404

        return form

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'payment': self.kwargs['payment'],
            'form': self.get_payment_form()
        })
        return context 

# Sprawdzanie kodu
class WalletPaymentFinish(generic.TemplateView):
    template_name = 'accounts/wallet/finish.html'

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        value = self.request.POST.get('value')
        context.update({
            'sms': SMSNumber.objects.get(pk=value)
        })
        return self.render_to_response(context=context)

    def get_return_code_form(self):
        return ReturnCodeForm()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'payment': self.kwargs['payment'],
            'form': self.get_return_code_form()
        })
        return context


# Finalizacja doładowania portfela
class WalletSuccess(generic.View):
    def post(self, request, *args, **kwargs):
        if self.kwargs['payment'] == 'sms':
            code = self.request.POST.get('code')
            user = self.request.user
            data = {
                'client_id': settings.LS_CLIENT_ID,
                'pin': settings.LS_CLIENT_PIN,
                'code': code
            }
            if len(code) == 8:
                response = requests.post(settings.LS_API_SMS_URL, data=data)
                if response.status_code >= 200 and response.status_code < 300:
                    row = urllib.parse.parse_qs(response.text)
                    # * dodać -> row['read_count'][0] == 0
                    if row['status'][0] == 'OK':
                        value_to_add = SMSNumber.objects.get(
                            number=row['number'][0]).value
                        user.add_cash(value_to_add)

                        PaymentHistory.objects.create(
                            user=user,
                            target=user,
                            change="+%.2f zł" % (value_to_add),
                            description="Doładowanie konta na %.2f zł" % (
                                value_to_add),
                            type='SMS'
                        )
                        messages.success(
                            self.request,
                            "Pomyślnie doładowano portfel na kwote %.2f zł" % (
                                value_to_add
                            )
                        )
                        return redirect(
                            reverse('accounts:wallet-index')
                        )
                    else:
                        messages.error(
                            self.request, "Podany kod jest błędny"
                        )
                        return redirect(
                            reverse(
                                'accounts:wallet-payment', kwargs={'payment': 'sms'}
                            )
                        )
                else:
                    messages.error(
                        self.request, "Wystąpił problem"
                    )
                    return redirect(
                        reverse(
                            'accounts:wallet-payment', kwargs={'payment': 'sms'}
                        )
                    )
            else:
                messages.error(
                    self.request, "Podany kod jest za krótki"
                )
                return redirect(
                    reverse(
                        'accounts:wallet-payment', kwargs={'payment': 'sms'}
                    )
                )

        elif self.kwargs['payment'] == 'promotion_code':
            try:
                code = PromotionCode.objects.get(
                    code=self.request.POST.get('code'))
            except PromotionCode.DoesNotExist:
                messages.error(self.request, "Podany kod jest błędny")
                return redirect(
                    reverse(
                        'accounts:wallet-payment', kwargs={'payment': 'promotion_code'}
                    )
                )
            user = self.request.user
            if code.multi:
                if code.user.filter(pk=user.pk):
                    messages.error(
                        self.request, "Kod został już wykorzystany przez ciebie")
                    return redirect(
                        reverse(
                            'accounts:wallet-payment', kwargs={'payment': 'promotion_code'}
                        )
                    )
                else:
                    code.user.add(user)
                    code.save()
                    user.add_cash(code.value)
                    PaymentHistory.objects.create(
                        user=user,
                        target=user,
                        change="+%.2f zł" % (code.value),
                        description="Doładowanie konta na %.2f zł" % (
                            code.value),
                        type='Kod promocyjny'
                    )
                    messages.success(
                        self.request,
                        "Pomyślnie doładowano portfel na kwote %.2f zł"
                        % (code.value)
                    )
                    return redirect(
                        reverse('accounts:wallet-index')
                    )
            else:
                if code.read_count == 0:
                    user.add_cash(code.value)
                    code.read_count += 1
                    code.save()
                    PaymentHistory.objects.create(
                        user=user,
                        target=user,
                        change="+%.2f zł" % (code.value),
                        description="Doładowanie konta na %.2f zł" % (
                            code.value),
                        type='Kod promocyjny'
                    )
                    messages.success(
                        self.request,
                        "Pomyślnie doładowano portfel na kwote %.2f zł"
                        % (code.value)
                    )
                    return redirect(
                        reverse('accounts:wallet-index')
                    )
                else:
                    messages.error(self.request, "Kod został już wykorzystany")
                    return redirect(
                        reverse(
                            'accounts:wallet-payment', kwargs={'payment': 'promotion_code'}
                        )
                    )

        elif self.kwargs['payment'] == 'przelew':
            code = self.request.POST.get('code')
            user = self.request.user
            data = {
                'client_id': settings.LS_CLIENT_ID,
                'pin': settings.LS_CLIENT_PIN,
                'code': code
            }
            if len(code) == 8:
                response = requests.post(settings.LS_API_SMS_URL, data=data)
                if response.status_code >= 200 and response.status_code < 300:
                    row = urllib.parse.parse_qs(response.text)
                    # * dodać -> row['read_count'][0] == 0
                    if row['status'][0] == 'OK':
                        user.add_cash(row['kwota'])
                        messages.success(
                            self.request,
                            "Pomyślnie doładowano portfel na kwote %s"
                            % (row['kwota'])
                        )
                        return redirect(reverse('accounts:wallet-index'))
                    else:
                        messages.error(
                            self.request,
                            "Podany kod jest błędny"
                        )
                        return redirect(
                            reverse(
                                'accounts:wallet-payment', kwargs={'payment': 'sms'}
                            )
                        )
                else:
                    messages.error(self.request, "Wystąpił problem")
                    return redirect(reverse('accounts:wallet-payment', kwargs={'payment': 'sms'}))
            else:
                messages.error(self.request, "Podany kod jest za krótki")
                return redirect(reverse('accounts:wallet-payment', kwargs={'payment': 'sms'}))

        else:
            messages.error(
                self.request, "Nie znaleziono takiej metody platnosci"
            )
            return redirect(reverse('accounts:wallet-index'))

# Transfer pieniędzy dla innego użytkownika


class WalletTransferMoney(generic.FormView, FormMixin):
    template_name = 'accounts/wallet/transfer.html'
    form_class = WalletTransfer

    def get_success_url(self):
        return reverse('accounts:wallet-transfer')

    def form_valid(self, form):
        user = self.request.user
        if user.cash and form.cleaned_data['value'] > 0 and form.cleaned_data['value'] <= user.cash:
            try:
                target = User.objects.get(username=form.cleaned_data['target'])
                target_exists = True
            except User.DoesNotExist:
                messages.error(self.request, "Podany użytkownik nie istnieje")
                target_exists = False
            value = 0.95 * float(form.cleaned_data['value'])
            if target_exists:
                if target != user:
                    target.add_cash(value)
                    user.remove_cash(form.cleaned_data['value'])
                    messages.success(
                        self.request, "Przekazałeś %.2f zł użytkownikowi %s" % (value, target))
                    history_user = PaymentHistory()
                    history_user.user = user
                    history_user.target = target
                    history_user.change = "-%.2f zł" % (value)
                    history_user.description = "Przekazałeś %.2f zł" % (value)
                    history_user.type = 'Przekaz dla użytkownika'
                    history_user.save()
                    history_target = PaymentHistory()
                    history_target.user = target
                    history_target.target = user
                    history_target.change = "+%.2f zł" % (value)
                    history_user.type = 'Przekaz dla użytkownika'
                    history_target.description = "Otrzymałeś %.2f zł" % (value)
                    history_target.save()
                else:
                    messages.error(
                        self.request, "Nie możesz wysłać pieniedzy do samego siebie")
        if form.cleaned_data['value'] <= 0:
            messages.error(self.request, "Kwota musi być większa od 0")
        if form.cleaned_data['value'] > user.cash:
            messages.error(
                self.request, "Kwota nie może być większa niż taka jaką posiadasz")
        return super().form_valid(form)

# Historia porftela uzytokwnika


class WalletPaymentHistory(generic.TemplateView):
    template_name = 'accounts/wallet/history.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        digg_paginator = DiggPaginator(PaymentHistory.objects.filter(
            user=self.request.user).order_by('-date'), 10)
        page = self.request.GET.get('page')
        context.update({
            'data_with_paginate': digg_paginator.get_page(page)
        })
        return context

# Zakupy uzytkownika


class MyShopping(generic.TemplateView):
    template_name = 'accounts/myshopping.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        premium_cache = PremiumCache.objects.filter(
            nick=self.request.user.steamid32).order_by('-pk')
        digg_paginator = DiggPaginator(premium_cache, 10)
        page = self.request.GET.get('page')
        context.update({
            'data_with_paginate': digg_paginator.get_page(page),
        })
        return context
