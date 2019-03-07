from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from accounts.models import MyGroup

class Command(BaseCommand):
    help = 'Instaluje domyślne grupy'

    def handle(self, *args, **options):
        wlasciciel = MyGroup.objects.create(pk=1, name='Właściciel')
        uzytkownik = MyGroup.objects.create(pk=2, name='Użytkownik')
        moderator = MyGroup.objects.create(pk=3, name='Moderator')
        opiekun_globalny = MyGroup.objects.create(pk=4, name='Opiekun Globalny')
        opiekun_serwera = MyGroup.objects.create(pk=5, name='Opiekun Serwera')

        groups_list = [
            uzytkownik,
            moderator,
        ]

        full_groups_list = [
            wlasciciel,
            opiekun_globalny,
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

        for group in full_groups_list:
            perms = Permission.objects.all()
            group.permissions.set(perms)

        self.stdout.write(self.style.SUCCESS('Instalacja przebiegła pomyślnie'))
