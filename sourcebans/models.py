from django.db import models
from servers.models import Server
from django_unixdatetimefield import UnixDateTimeField
from django.utils.translation import gettext_lazy as _

class Ban(models.Model):
    name = models.CharField(verbose_name="Nick", max_length=128)
    authid = models.CharField(verbose_name="Steam ID", max_length=32)
    ip = models.CharField(_('IP'), max_length=32, null=True)
    created = UnixDateTimeField()
    ends = UnixDateTimeField()
    length = models.IntegerField()
    reason = models.TextField(max_length=500)
    admin = models.IntegerField()
    adminIp = models.CharField(max_length=32)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    ureason = models.IntegerField()

    def __str__(self):
        return self.name + '('+self.authid+')'

    class Meta:
        db_table = 'sourcebans_bans' 
        verbose_name = 'SourceBans - Ban'
        verbose_name_plural = _('SourceBans - Bany')


class Comm(models.Model):
    name = models.CharField(verbose_name="Nick", max_length=128)
    authid = models.CharField(verbose_name="Steam ID", max_length=32)
    ip = models.CharField(_('IP'), max_length=32, null=True)
    created = UnixDateTimeField()
    ends = UnixDateTimeField()
    length = models.IntegerField()
    reason = models.TextField(max_length=500)
    admin = models.IntegerField()
    adminIp = models.CharField(max_length=32)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    ureason = models.IntegerField()

    
    def __str__(self):
        return self.name + '('+self.authid+')'

    class Meta:
        db_table = 'sourcebans_comms' 
        verbose_name = 'SourceBans - Komunikacja'
        verbose_name_plural = _('SourceBans - Komunikacja')