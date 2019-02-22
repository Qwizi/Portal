from django import forms
from django.forms import ModelChoiceField, ModelForm
from .models import Custom_ChatColors, Sm_Admins, Sm_Groups

class CCCForm(forms.Form):
    identity = forms.CharField(max_length=32)
    flag = forms.CharField(max_length=1, required=False)
    tag = forms.CharField(max_length=32)
    tagcolor = forms.CharField(max_length=8, required=False)
    namecolor = forms.CharField(max_length=8, required=False)
    textcolor = forms.CharField(max_length=8, required=False)
    alias = forms.CharField(max_length=50, required=False)

    def __init__(self, *args, **kwargs):
        super(CCCForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class AdminsForm(forms.Form):
    STEAM = 'STEAM'
    NAME = 'NAME'
    IP = 'IP'
    AUTH_TYPE_CHOICE = (
        (STEAM, 'steam'),
        (NAME, 'name'),
        (IP, 'ip')
    )
    authtype = forms.ChoiceField(choices=AUTH_TYPE_CHOICE)
    identity = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, required=False)
    flags = forms.CharField(max_length=30, required=False)
    name = forms.CharField(max_length=30)
    immunity = forms.IntegerField(required=False)
    groups = forms.ChoiceField(choices=(), required=False)
    
    def __init__(self, foo_choices, *args, **kwargs):
        super(AdminsForm, self).__init__(*args, **kwargs)
        self.fields['groups'].choices = foo_choices
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class GroupsForm(forms.Form):
    flags = forms.CharField(max_length=30)
    name = forms.CharField(max_length=120)
    immunity_level = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        super(GroupsForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
    
