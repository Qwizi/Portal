from django import template
from accounts.models import MyGroup
from django.utils.safestring import mark_safe
register = template.Library()

@register.filter(name="login_format")
def login_format(user_object):
    replaced_display_name = user_object.display_group.login_format.replace('{username}', user_object.username)
    return mark_safe(replaced_display_name)

@register.filter(name="groupname_format")
def groupname_format(user_groupname_object):
    replaced_user_groupname = user_groupname_object.login_format.replace('{username}', user_groupname_object.name)
    return mark_safe(replaced_user_groupname)