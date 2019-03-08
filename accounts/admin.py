from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, MyGroup

class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 
            'steamid64', 
            'steamid32', 
            'email', 
            'is_active', 
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'display_group'
        )

class UserChangeForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 
            'steamid64', 
            'steamid32', 
            'email', 
            'is_active', 
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'cash',
            'display_group'
        )

class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserChangeForm

    list_display = ('username', 'steamid64', 'steamid32', 'is_staff', 'is_active', 'is_superuser')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('username', 'steamid64', 'steamid32')}),
        ('Personal info', {'fields': ('email', 'cash')}),
        ('Permissions', {'fields': ('is_staff', 'is_superuser', 'display_group', 'groups')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'steamid64', 'email', 'is_staff')}
        ),
    )
    search_fields = ('steamid64', 'steamid32')
    ordering = ('username',)
    filter_horizontal = ()

class GroupAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)

    def formfield_for_manytomany(self, db_field, request=None, **kwargs):
        if db_field.name == 'permissions':
            qs = kwargs.get('queryset', db_field.remote_field.model.objects)
            # Avoid a major performance hit resolving permission names which
            # triggers a content_type load:
            kwargs['queryset'] = qs.select_related('content_type')
        return super().formfield_for_manytomany(db_field, request=request, **kwargs)

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(MyGroup, GroupAdmin)
admin.site.register(Permission)