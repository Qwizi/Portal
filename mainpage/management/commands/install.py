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

        groups_list = (
            uzytkownik,
            moderator,
            opiekun_globalny,
        )

        full_groups_list = (
            wlasciciel,
            opiekun_globalny,
        )

        accounts_ct = ContentType.objects.get(app_label='accounts', model='User')
        shop_ct = ContentType.objects.get(app_label='shop', model='Bonus')
        application_ct = ContentType.objects.get(app_label='user_centrum', model='Application')

        perms_list = (
            accounts_ct, (
                'view_account',
                'view_wallet',
                'add_wallet',
                'transfer_wallet',
                'view_myshopping'
            ),
            shop_ct, (
                'view_bonus'
            )
        )

        account_perms_list = (
            'view_account',
            'view_wallet',
            'add_wallet',
            'transfer_wallet',
            'view_myshopping'
        )
        shop_perms_list = 'view_bonus'

        """
        for perm in account_perms_list:
            account_perms = Permission.objects.get(codename=perm, content_type=accounts_ct)
            for group in groups_list:
                group.permissions.add(account_perms)
        """

        for perm in perms_list:
            account_perms = Permission.objects.get(codename=perm[1], content_type=perm[0])
            for group in groups_list:
                group.permissions.add(account_perms)

        shop_perms = Permission.objects.get(codename=shop_perms_list, content_type=shop_ct)
        for group in groups_list:
            group.permissions.add(shop_perms)

        for group in full_groups_list:
            perms = Permission.objects.all()
            group.permissions.add(perms)

        self.stdout.write(self.style.SUCCESS('Instalacja przebiegła pomyślnie'))
