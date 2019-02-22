from django import template
import requests
register = template.Library()


@register.simple_tag
def get_admingroups_name(*args):

    url = 'http://localhost:8000/api/{}/admins-groups/{}'.format(args[0], args[1])
    response = requests.get(url)
    if response.status_code == 200:
        row = response.json()
        return row['name']
    else:
        return None