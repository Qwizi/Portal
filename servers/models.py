from django.db import models
from django.db.models.signals import post_save
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from accounts.models import User, MyGroup

class Server(models.Model):
    name = models.CharField(verbose_name='Nazwa serwera', max_length=64, default='Nazwa')
    banner = models.ImageField(verbose_name='Banner', null=True, blank=True, upload_to='banners/')
    ip = models.CharField(verbose_name='IP', max_length=64)
    port = models.CharField(verbose_name='Port', max_length=64, null=True)
    tag = models.CharField(verbose_name='Tag serwera', max_length=64, null=True)
    managers = models.ManyToManyField(User, blank=True)

    class Meta:
        verbose_name = 'Serwer'
        verbose_name_plural = 'Serwery'

    def __str__(self):
        return self.name

def create_server_groups(sender, **kwargs):
    if kwargs['created']:
        admin_group = MyGroup.objects.create(name="Admin {}".format(kwargs['instance'].tag), login_format="<span style=\"color: #1b64e1\">{username}</span>", showteam=True)
        junioradmin_group = MyGroup.objects.create(name="Junior Admin {}".format(kwargs['instance'].tag), login_format="<span style=\"color: #83bd04\">{username}</span>", showteam=True)

        groups_list = [
            admin_group,
            junioradmin_group,
        ]
        
        shop_ct = ContentType.objects.get(app_label='shop', model='Bonus')
        application_ct = ContentType.objects.get(app_label='user_centrum', model='Application')
        accounts_ct = ContentType.objects.get(app_label='accounts', model='User')

        account_codename_list = [
            'view_account',
            'view_wallet',
            'add_wallet',
            'transfer_wallet'
        ]

        for codename in account_codename_list:
            account_perm = Permission.objects.get(codename=codename, content_type=accounts_ct)
            for group in groups_list:
                group.permissions.add(account_perm)

        shop_perms = Permission.objects.get(codename='view_bonus', content_type=shop_ct)
        for group in groups_list:
            group.permissions.add(shop_perms)

post_save.connect(create_server_groups, sender=Server)