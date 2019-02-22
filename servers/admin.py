from django.contrib import admin
from .models import Server

class Servers(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('managers',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'managers':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)
admin.site.register(Server, Servers)