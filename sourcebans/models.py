from django.db import models
from servers.models import Server
from django_unixdatetimefield import UnixDateTimeField
from django.utils.translation import gettext_lazy as _

class Bans(models.Model):
    ip = models.CharField(
        _('IP'),
        max_length=32, 
        null=True
    )
    authid = models.CharField(verbose_name="Steam ID", max_length=32)
    name = models.CharField(verbose_name="Nick", max_length=128)
    created = UnixDateTimeField()
    ends = UnixDateTimeField()
    length = models.IntegerField()
    reason = models.TextField(max_length=500)
    aid = models.IntegerField()
    adminIp = models.CharField(max_length=32)
    sid = models.ForeignKey(Server, on_delete=models.CASCADE)
    country = models.CharField(max_length=4)
    RemovedBy = models.IntegerField()
    RemoveType = models.CharField(max_length=3)
    RemovedOn = models.IntegerField()
    type = models.IntegerField()
    ureason = models.IntegerField()

    def __str__(self):
        return self.name + '('+self.authid+')'

    class Meta: 
        verbose_name = _('ban')
        verbose_name_plural = _('lista banów')


class Comms(models.Model):
    ip = models.CharField(verbose_name="IP", max_length=32, null=True)
    authid = models.CharField(verbose_name="Steam ID", max_length=32)
    name = models.CharField(verbose_name="Nazwa", max_length=128)
    created = UnixDateTimeField()
    ends = UnixDateTimeField()
    length = models.IntegerField()
    reason = models.TextField(max_length=500)
    aid = models.IntegerField()
    adminIp = models.CharField(max_length=32)
    sid = models.ForeignKey(Server, on_delete=models.CASCADE)
    country = models.CharField(max_length=4)
    RemovedBy = models.IntegerField()
    RemoveType = models.CharField(max_length=3)
    RemovedOn = models.IntegerField()
    type = models.IntegerField()
    ureason = models.IntegerField()