from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import _user_get_all_permissions, _user_has_perm, _user_has_module_perms, Permission, PermissionManager
from django.contrib.contenttypes.models import ContentType
from decimal import *
from django.urls import reverse
from django.apps import apps
from collections import defaultdict
from rest_framework.authtoken.models import Token
import binascii
import os

class GroupManager(models.Manager):
    """
    The manager for the auth's Group model.
    """
    use_in_migrations = True

    def get_by_natural_key(self, name):
        return self.get(name=name)

class MyGroup(models.Model):
    name = models.CharField(_('name'), max_length=80, unique=True)
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('permissions'),
        blank=True,
    )
    login_format = models.CharField(max_length=512, default="{username}")

    objects = GroupManager()

    class Meta:
        verbose_name = _('Grupa')
        verbose_name_plural = _('Grupy')

    def __str__(self):
        return self.name

    def natural_key(self):
        return (self.name,)

class MyUserManager(models.Manager):
    def create_user(self, username, steamid64, steamid32, email, **extra_fields):
        user = self.model(
            username=username, 
            steamid64=steamid64, 
            steamid32=steamid32, 
            email=email,
        )
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, steamid64, steamid32, email, **extra_fields):
        user = self.create_user(
            username=username, 
            steamid64=steamid64, 
            steamid32=steamid32, 
            email=email
        )
        user.is_staff = True
        user.save(using=self._db)
        return user

    def get_by_natural_key(self, username):
        return self.get(**{self.model.USERNAME_FIELD: username})


class User(models.Model):
    username = models.CharField(_('Nick'), max_length=255, null=True)
    steamid64 = models.CharField(_('Steamid 64'), max_length=255, unique=True)
    steamid32 = models.CharField(_('Steamid 32'), max_length=255, unique=True, null=True, blank=True)
    email = models.CharField(_('E-mail'), max_length=255, unique=True, null=True, blank=True)
    avatar = models.CharField(_('Avatar'),max_length=255,null=True,blank=True)
    avatar_medium = models.CharField(_('Avatar Medium'),max_length=255,null=True,blank=True)
    avatar_full = models.CharField(_('Avatar Full'),max_length=255,null=True,blank=True)
    date_joined = models.DateTimeField(_('Data dołączenia'), default=timezone.now)
    cash = models.DecimalField(_('Pieniądze'),max_digits=19, decimal_places=2,default=0,)
    is_active = models.BooleanField(_('Jest aktywny?'), default=True)
    is_staff = models.BooleanField(_('Jest adminem?'), default=False)
    is_superuser = models.BooleanField(
        _('superuser status'),
        default=False,
        help_text=_(
            'Designates that this user has all permissions without '
            'explicitly assigning them.'
        ),
    )
    display_group = models.ForeignKey(MyGroup, on_delete=models.CASCADE, related_name="user_display_group_set", null=True)
    groups = models.ManyToManyField(
        MyGroup,
        verbose_name=_('groups'),
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        related_name="user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        help_text=_('Specific permissions for this user.'),
        related_name="user_set",
        related_query_name="user",
    )

    class Meta: 
        verbose_name = _('Uzytkownik')
        verbose_name_plural = _('Uzytkownicy')
        permissions = (
            ('view_account', 'Może przeglądać konto'),
            ('view_wallet', 'Może przeglądać portfel'),
            ('add_wallet', 'Może doladowywac portfel'),
            ('transfer_wallet', 'Może przekazywac pieniadze'),
            ('view_myshopping', 'Może przeglądać swoje zakupy')
        )

    USERNAME_FIELD = 'steamid64'
    REQUIRED_FIELDS = ['username', 'steamid32', 'email']

    objects = MyUserManager()

    def __str__(self):
        return self.username

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.username

    def get_group_permissions(self, obj=None):
        """
        Return a list of permission strings that this user has through their
        groups. Query all available auth backends. If an object is passed in,
        return only permissions matching this object.
        """
        permissions = set()
        for backend in auth.get_backends():
            if hasattr(backend, "get_group_permissions"):
                permissions.update(backend.get_group_permissions(self, obj))
        return permissions

    def get_all_permissions(self, obj=None):
        return _user_get_all_permissions(self, obj)

    def has_perm(self, perm, obj=None):
        """
        Return True if the user has the specified permission. Query all
        available auth backends, but return immediately if any backend returns
        True. Thus, a user who has permission from a single auth backend is
        assumed to have permission in general. If an object is provided, check
        permissions for that object.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)

    def has_perms(self, perm_list, obj=None):
        """
        Return True if the user has each of the specified permissions. If
        object is passed, check if the user has all required perms for it.
        """
        return all(self.has_perm(perm, obj) for perm in perm_list)

    def has_module_perms(self, app_label):
        """
        Return True if the user has any permissions in the given app label.
        Use similar logic as has_perm(), above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True

        return _user_has_module_perms(self, app_label)

    def get_cash(self):
        if self.is_anonymous is not None:
            return "%.2f zł" % (self.cash)

    def add_cash(self, cash):
        self.cash += Decimal(cash)
        self.save()
        return True

    def remove_cash(self, cash='2.0'):
        self.cash -= Decimal(cash)
        self.save()
        return True

class PaymentHistory(models.Model):
    USER = 'USER'
    SHOP = 'SHOP'
    SMS = 'SMS'
    CODE = 'CODE'
    TRANSFER = 'TRANSFER'
    TYPE_CHOICES = (
        (USER, 'Przekaz dla użytkownika'),
        (SHOP, 'Sklep'),
        (SMS, 'SMS'),
        (CODE, 'Kod promocyjny'),
        (TRANSFER, 'Przelew')
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user", null=True)
    target = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True, blank=True)
    change = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=50, null=True)
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=SHOP)
    def __str__(self):
        return self.target

    class Meta:
        verbose_name = 'PaymentHistory'
        verbose_name_plural = 'PaymentHistorys'

class Payment(models.Model):
    tag = models.CharField(max_length=30)
    name = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Platnosc'
        verbose_name_plural = 'Platnosci'