from django import forms

class SearchBans(forms.Form):
    steamid = forms.CharField(max_length=64)