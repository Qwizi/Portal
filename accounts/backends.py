import requests
from .models import User, MyGroup, Permission
from django.conf import settings
from django.contrib.auth import get_user_model
import random
import string

UserModel = get_user_model()


def randomstr(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class SteamBackend:
    def to_steamid32(self, steamid64):
        steamid64ident = 76561197960265728
        steamid = []
        steamid.append('STEAM_0:')
        steamidacct = int(steamid64) - steamid64ident

        if steamidacct % 2 == 0:
            steamid.append('0:')
        else:
            steamid.append('1:')
        steamid.append(str(steamidacct // 2))

        return ''.join(steamid)

    def authenticate(self, request, steamid64):
        try:
            # !!Pobieramy użytkownika przez steamid64
            user = User.objects.get(steamid64=steamid64)
        except User.DoesNotExist:
            base_url = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/'
            data = {
                'key': settings.STEAM_API_KEY,
                'steamids': steamid64
            }

            response = requests.get(base_url, params=data)
            raw_data = response.json()
            user = User(steamid64=steamid64)
            user.steamid32 = self.to_steamid32(steamid64)
            user.username = raw_data['response']['players'][0]['personaname']
            user.avatar = raw_data['response']['players'][0]['avatar']
            user.avatar_medium = raw_data['response']['players'][0]['avatarmedium']
            user.avatar_full = raw_data['response']['players'][0]['avatarfull']
            
            # Wysyłamy dane do bazy danych
            user.save()

            # dodajemy domyślną grupę użytkownikowi
            my_group = MyGroup.objects.get(pk=2)
            my_group.user_set.add(user)

        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def _get_user_permissions(self, user_obj):
        return user_obj.user_permissions.all()

    def _get_group_permissions(self, user_obj):
        user_groups_field = get_user_model()._meta.get_field('groups')
        user_groups_query = 'mygroup__%s' % user_groups_field.related_query_name()
        return Permission.objects.filter(**{user_groups_query: user_obj})

    def _get_permissions(self, user_obj, obj, from_name):
        """
        Return the permissions of `user_obj` from `from_name`. `from_name` can
        be either "group" or "user" to return permissions from
        `_get_group_permissions` or `_get_user_permissions` respectively.
        """
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()

        perm_cache_name = '_%s_perm_cache' % from_name
        if not hasattr(user_obj, perm_cache_name):
            if user_obj.is_superuser:
                perms = Permission.objects.all()
            else:
                perms = getattr(self, '_get_%s_permissions' %
                                from_name)(user_obj)
            perms = perms.values_list(
                'content_type__app_label', 'codename').order_by()
            setattr(user_obj, perm_cache_name, {
                    "%s.%s" % (ct, name) for ct, name in perms})
        return getattr(user_obj, perm_cache_name)

    def get_user_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from their
        `user_permissions`.
        """
        return self._get_permissions(user_obj, obj, 'user')

    def get_group_permissions(self, user_obj, obj=None):
        """
        Return a set of permission strings the user `user_obj` has from the
        groups they belong.
        """
        return self._get_permissions(user_obj, obj, 'group')

    def get_all_permissions(self, user_obj, obj=None):
        if not user_obj.is_active or user_obj.is_anonymous or obj is not None:
            return set()
        if not hasattr(user_obj, '_perm_cache'):
            user_obj._perm_cache = {
                *self.get_user_permissions(user_obj),
                *self.get_group_permissions(user_obj),
            }
        return user_obj._perm_cache

    def has_perm(self, user_obj, perm, obj=None):
        return user_obj.is_active and perm in self.get_all_permissions(user_obj, obj)

    def has_module_perms(self, user_obj, app_label):
        """
        Return True if user_obj has any permissions in the given app_label.
        """
        return user_obj.is_active and any(
            perm[:perm.index('.')] == app_label
            for perm in self.get_all_permissions(user_obj)
        )
