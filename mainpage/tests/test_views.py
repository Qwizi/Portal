from django.test import TestCase, Client
from django.urls import reverse
from mainpage.models import Rule
from servers.models import Server
from django.test import RequestFactory
from mainpage import views
