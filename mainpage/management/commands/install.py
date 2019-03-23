from django.core.management.base import BaseCommand, CommandError
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from accounts.models import MyGroup

class Command(BaseCommand):
    help = 'Instaluje domyślne grupy'

    def handle(self, *args, **options):
        wlasciciel = MyGroup.objects.create(pk=1, name='Właściciel', login_format="<span style=\"color: red\">{username}</span>", usertitle="Właściciel", showteam=True, disporder=1)
        uzytkownik = MyGroup.objects.create(pk=2, name='Użytkownik', login_format="<span style=\"color: gray\">{username}</span>", usertitle="Użytkownik")
        moderator = MyGroup.objects.create(pk=3, name='Moderator', login_format="<span style=\"color: green\">{username}</span>", usertitle="Moderator", showteam=True, disporder=3)
        opiekun_globalny = MyGroup.objects.create(pk=4, name='Opiekun Globalny', login_format="<span style=\"color: black\">{username}</span>", usertitle="Opiekun Globalny", showteam=True, disporder=2)
        opiekun_serwera = MyGroup.objects.create(pk=5, name='Opiekun Serwera', login_format="<span style=\"color: purple\">{username}</span>", usertitle="Opiekun Serwera", showteam=True, disporder=5)
        shark = MyGroup.objects.create(pk=6, name='Shark', login_format="<span style=\"color: #00aeff\"><i class=\"fas fa-gem\"></i> {username}</span>", usertitle="Shark")
        zbanowany =  MyGroup.objects.create(pk=7, name='Zbanowany', login_format="<span style=\"color: #e0e0e0\"><s>{username}</s></span>", usertitle="Zbanowany")

        groups_list = [
            uzytkownik,
            moderator,
            shark
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
