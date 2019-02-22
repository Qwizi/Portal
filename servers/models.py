from django.db import models
from accounts.models import User

class Server(models.Model):
    name = models.CharField(
        verbose_name='Nazwa serwera',
        max_length=64,
        default='Nazwa'
    )
    banner = models.ImageField(
        verbose_name='Banner',
        null=True,
        blank=True,
        upload_to='banners/'
    )
    ip = models.CharField(
        verbose_name='IP',
        max_length=64
    )
    port = models.CharField(
        verbose_name='Port',
        max_length=64,
        null=True
    )
    tag = models.CharField(
        verbose_name='Tag serwera',
        max_length=64,
        null=True
    )
    managers = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Serwer'
        verbose_name_plural = 'Serwery'

    def __str__(self):
        return self.name
