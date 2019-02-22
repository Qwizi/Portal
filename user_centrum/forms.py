from django.forms import ModelForm
from django import forms
from .models import Application, ApplicationComments
class ApplicationModelFormCreate(ModelForm):
    class Meta:
        model = Application
        fields = ('owner', 'type','server','name', 'age','microphone','reason',)

    def __init__(self, *args, **kwargs):
        super(ApplicationModelFormCreate, self).__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.widgets.HiddenInput()
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ApplicationModelForm(ModelForm):
    class Meta:
        model = Application
        fields = ('type','server','name', 'age','microphone','reason',)

    def __init__(self, *args, **kwargs):
        super(ApplicationModelForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

class ApplicationCommentsModelFormCreate(ModelForm):
    class Meta:
        model = ApplicationComments
        fields = ('application', 'owner', 'content', 'owner_name', 'owner_avatar', )

    def __init__(self, *args, **kwargs):
        super(ApplicationCommentsModelFormCreate, self).__init__(*args, **kwargs)
        self.fields['owner'].widget = forms.widgets.HiddenInput()
        self.fields['application'].widget = forms.widgets.HiddenInput()
        self.fields['owner_name'].widget = forms.widgets.HiddenInput()
        self.fields['owner_avatar'].widget = forms.widgets.HiddenInput()
        self.fields['content'].widget.attrs['rows'] = 3
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

            