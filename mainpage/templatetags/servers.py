from django import template
from django.conf import settings
import requests
from steam import SteamQuery
register = template.Library()

@register.simple_tag
def get_server_info(*args, **kwargs):
    
    server_obj = SteamQuery(args[0], args[1], 5)
    return_dictionary = server_obj.query_game_server()

    if kwargs['type'] == 'players' and return_dictionary['online'] is True:
        return_value = return_dictionary['players']
    elif kwargs['type'] == 'max_players' and return_dictionary['online'] is True:
        return_value = return_dictionary['max_players']
    elif kwargs['type'] == 'map' and return_dictionary['online'] is True:
        return_value = return_dictionary['map']
    if return_dictionary['online'] is True:
        return return_value
    else:
        return 'None'