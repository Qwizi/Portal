from django import forms
from django.forms import ModelChoiceField
from .models import Bonus
from servers.models import Server


class ShopForm(forms.Form):
    nick = forms.CharField(max_length=512, widget=forms.HiddenInput)
    server = forms.IntegerField(widget=forms.HiddenInput)
    service = forms.IntegerField(widget=forms.HiddenInput)
    days = forms.IntegerField(widget=forms.HiddenInput)
    flags = forms.CharField(max_length=512, widget=forms.HiddenInput)


class ShopAddForm(forms.Form):
    nick = forms.CharField(max_length=512)
    server = ModelChoiceField(queryset=Server.objects.all())
    bonus = ModelChoiceField(queryset=Bonus.objects.all())
    days = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
