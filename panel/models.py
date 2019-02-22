from django.db import models
from servers.models import Server

class Module(models.Model):
    name = models.CharField(max_length=50)
    tag = models.CharField(max_length=50)
    servers = models.ManyToManyField(Server)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Panel - Moduł'
        verbose_name_plural = 'Panel - Moduły'