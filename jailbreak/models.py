from django.db import models


class StorePlayer(models.Model):
    authid = models.CharField(max_length=32, unique=True)
    name = models.CharField(max_length=64)
    credits = models.BigIntegerField()
    date_of_join = models.DateField()
    date_of_last_join = models.DateField()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'store_players'
        verbose_name = 'Store - Gracz'
        verbose_name_plural = 'Store - Gracze'


class StoreItem(models.Model):
    player_id = models.IntegerField()
    type = models.CharField(max_length=16)
    unique_id = models.CharField(max_length=256)
    date_of_purchase = models.DateField()
    date_of_expiration = models.DateField()
    price_of_purchase = models.IntegerField()

    def __str__(self):
        return "%d | %d " % (self.player_id, self.unique_id)

    class Meta:
        db_table = 'store_items'
        verbose_name = 'Store - Przedmiot'
        verbose_name_plural = 'Store - Przedmity'


class StoreEquipment(models.Model):
    player_id = models.IntegerField()
    type = models.CharField(max_length=16)
    unique_id = models.CharField(max_length=256)
    slot = models.IntegerField()

    def __str__(self):
        return self.unique_id

    class Meta:
        db_table = 'store_equipment'
        verbose_name = 'Store - Ekwipunek'
        verbose_name_plural = 'Store - Ekwipunki'


class CustomChatColor(models.Model):
    alias = models.CharField(max_length=50, null=True, blank=True)
    identity = models.CharField(max_length=32, unique=True)
    flag = models.CharField(max_length=1, null=True, blank=True)
    tag = models.CharField(max_length=32)
    tagcolor = models.CharField(max_length=8, null=True, blank=True)
    namecolor = models.CharField(max_length=8, null=True, blank=True)
    textcolor = models.CharField(max_length=8, null=True, blank=True)

    def __str__(self):
        return "%s | %s " % (self.identity, self.alias)

    class Meta:
        db_table = 'custom_chatcolors'
        verbose_name = 'Kolor czatu'
        verbose_name_plural = 'Kolory czatu'


class SourceModGroup(models.Model):
    flags = models.CharField(max_length=30)
    name = models.CharField(max_length=120)
    immunity_level = models.PositiveIntegerField()

    class Meta:
        db_table = 'sm_groups'
        verbose_name = 'SourceMod - Grupa'
        verbose_name_plural = 'SourceMod - Grupy'


class SourceModAdmin(models.Model):
    STEAM = 'STEAM'
    NAME = 'NAME'
    IP = 'IP'
    AUTH_TYPE_CHOICE = (
        (STEAM, 'steam'),
        (NAME, 'name'),
        (IP, 'ip')
    )
    authtype = models.CharField(
        max_length=50, choices=AUTH_TYPE_CHOICE, default=STEAM)
    identity = models.CharField(max_length=65, null=False)
    password = models.CharField(max_length=65, null=True, blank=True)
    flags = models.CharField(max_length=30, null=True, blank=True)
    name = models.CharField(max_length=65, null=False)
    immunity = models.PositiveIntegerField(null=True, blank=True)
    groups = models.ManyToManyField(SourceModGroup, blank=True, related_name='groups_set')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sm_admins'
        verbose_name = 'SourceMod - Admin'
        verbose_name_plural = 'SourceMod - Admini'


class SourceModGroupImmunity(models.Model):
    group = models.ForeignKey(SourceModGroup, on_delete=models.CASCADE)
    other_id = models.PositiveIntegerField()

    class Meta:
        db_table = 'sm_group_immunity'
        verbose_name = 'SourceMod - Immunitet Grupy'
        verbose_name_plural = 'SourceMod - Immunitet Grup'


class SourceModOverride(models.Model):
    COMMAND = 'command'
    GROUP = 'group'
    CHOICES = (
        (COMMAND, 'command'),
        (GROUP, 'group')
    )
    type = models.CharField(max_length=50, choices=CHOICES, default=COMMAND)
    name = models.CharField(max_length=32)
    flags = models.CharField(max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'sm_overrides'
        verbose_name = 'SourceMod - Override'
        verbose_name_plural = 'SourceMod - Overrides'


class SourceModGroupOverride(models.Model):
    COMMAND = 'command'
    GROUP = 'group'
    CHOICES_TYPE = (
        (COMMAND, 'command'),
        (GROUP, 'group')
    )
    ALLOW = 'allow'
    DENY = 'deny'
    CHOICES_ACCESS = (
        (ALLOW, 'allow'),
        (DENY, 'deny')
    )
    group = models.ForeignKey(SourceModGroup, on_delete=models.CASCADE)
    type = models.CharField(
        max_length=50, choices=CHOICES_TYPE, default=COMMAND)
    name = models.CharField(max_length=32)
    access = models.CharField(
        max_length=50, choices=CHOICES_ACCESS, default=ALLOW)

    def __str__(self):
        return

    class Meta:
        db_table = 'sm_group_overrides'
        verbose_name = 'SourceMod - Group Override'
        verbose_name_plural = 'SourceMod - Groups Overrides'
