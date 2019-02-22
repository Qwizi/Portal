from django.shortcuts import render
from django.conf import Settings
from .models import Server
import requests
import json

def servers_list(request):
    servers = Server.objects.all()
    data = {
        'client_id': Settings.LS_CLIENT_ID,
        'pin': Settings.LS_CLIENT_PIN,
        'server_id': '334'
    }
    response = requests.post(Settings.LS_URL, data=data)

    if response.status_code == 200:
          server = response.json()
          server['success'] = True
    else:
           server['success'] = False
    if response.status_code == 404:
         server['message'] = "Nie znaleziono serwera"
    else:
        server['message'] = 'Api nie dostępne'
        server['success'] = False
        return server


    return render(request, 'servers/servers_list.html', {
        'server_name': server['name'],
        'server_players': server['players'],
        'server_maxplayers': server['maxplayers'],
        'server_map': server['map'],
        'servers': servers
    })
