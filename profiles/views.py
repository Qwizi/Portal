from django.shortcuts import render, get_object_or_404
from django.views import generic
from accounts.models import User

class ProfileIndex(generic.DetailView):
    template_name = 'profiles/index.html'
    context_object_name = 'user_profile'

    def get_object(self):
        return get_object_or_404(User, pk=self.kwargs['pk'])
