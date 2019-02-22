from django.shortcuts import render
from django.views import generic
from digg_paginator import DiggPaginator
from django.contrib import messages
from sourcebans import models

import re


class BansIndex(generic.ListView):
    queryset = models.Bans.objects.all().order_by('-created')
    context_object_name = 'ban_list'
    template_name = 'sourcebans/index.html'

    def get_paginate_data(self):
        digg_paginator = DiggPaginator(self.queryset, 15)
        page = self.request.GET.get('page')
        return digg_paginator.get_page(page)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_with_paginate'] = self.get_paginate_data()
        return context


def search_bans(request):
    if request.method == 'GET':
        steamid = request.GET['steamid']
        steamid = re.sub(r"\s+", "", steamid, flags=re.UNICODE)
        bans_list = Bans.objects.filter(authid=steamid).order_by('-created')

        paginator = DiggPaginator(bans_list, 15)
        page = request.GET.get('page')
        bans = paginator.get_page(page)

    return render(request, 'sourcebans/search_bans.html', {
        'bans': bans,
        'steamid': steamid
    })
