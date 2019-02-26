from django.views import generic
from digg_paginator import DiggPaginator
from sourcebans.models import Ban


class BansIndex(generic.ListView):
    queryset = Ban.objects.all().order_by('-created')
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
