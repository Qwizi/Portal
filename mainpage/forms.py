from django.forms import ModelForm
from jailbreak import models

class CCCForm(ModelForm):
    class Meta:
        model = models.Custom_ChatColors
        fields = '__all__'