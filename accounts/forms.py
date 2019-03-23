from django import forms
from django.forms import ModelForm, ModelChoiceField
from shop.models import SMSNumber

class WalletTransfer(forms.Form):
    target = forms.CharField(max_length=512, label="Użytkownik")
    value = forms.DecimalField(label="Pieniądze", decimal_places=2)

    def __init__(self, *args, **kwargs):
        super(WalletTransfer, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class SMSNumberForm(forms.Form):
    value = forms.ModelChoiceField(queryset=SMSNumber.objects.all(), label="Wartość")

    def __init__(self, *args, **kwargs):
        super(SMSNumberForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class PromotionCodeForm(forms.Form):
    code = forms.CharField(max_length=8, label="Kod")

    def __init__(self, *args, **kwargs):
        super(PromotionCodeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ReturnCodeForm(forms.Form):
    code = forms.CharField(max_length=8, label="Kod")

    def __init__(self, *args, **kwargs):
        super(ReturnCodeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
