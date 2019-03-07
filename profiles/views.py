from django.shortcuts import render
from django.views import generic
from accounts.models import User

class ProfileIndex(generic.DetailView):
    template_name = 'profiles/index.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return User.objects.get(pk=self.kwargs['pk'])
