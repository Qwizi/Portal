from django.db import models
from django.utils.translation import gettext_lazy as _
from servers.models import Server
from django.conf import settings
from django_unixdatetimefield import UnixDateTimeField
from decimal import *

class Payment(models.Model):

    def __str__(self):
        pass

    class Meta:
        db_table = ''
        managed = True
        verbose_name = 'Sklep -'
        verbose_name_plural = 'Payments'

class Premium(models.Model):
    nick = models.CharField(max_length=512, null=False)
    flags = models.CharField(max_length=512, null=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)

    def __str__(self):
        return self.nick

    class Meta:
        db_table = 'shop_premium'
        verbose_name = 'Premium'
        verbose_name_plural = 'Premiums'


class Price(models.Model):
    value = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0
    )

    def __str__(self):
        return "%.2f" % (Decimal(self.value))

    class Meta:
        db_table = 'shop_price'
        verbose_name = 'Cena'
        verbose_name_plural = 'Ceny'


class SMSNumber(models.Model):
    vat = models.CharField(max_length=512, null=False, blank=False)
    value = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0)
    number = models.CharField(max_length=512, null=False)

    def __str__(self):
        return "%s | %s" % (self.value, self.number)

    class Meta:
        db_table = 'shop_sms_numbers'
        verbose_name = 'Numer SMS'
        verbose_name_plural = 'Numery SMS'


class Bonus(models.Model):
    name = models.CharField(max_length=512)
    tag = models.CharField(max_length=512)
    flags = models.CharField(max_length=512)
    description = models.TextField(null=True)
    description_full = models.TextField(null=True)
    servers = models.ManyToManyField(Server)

    class Meta:
        db_table = 'shop_bonus'
        verbose_name = 'Bonus'
        verbose_name_plural = 'Bonusy'

    def __str__(self):
        return "%s | %s | %s " % (self.name, self.tag, self.flags)


class Service(models.Model):
    price = models.ForeignKey(Price, on_delete=models.CASCADE)
    days = models.IntegerField()
    bonus = models.ForeignKey(Bonus, on_delete=models.CASCADE, null=True)
    promotion_price = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0
    )

    class Meta:
        db_table = 'shop_service'
        verbose_name = 'Usluga'
        verbose_name_plural = 'Uslugi'

    def __str__(self):
        return "%s | %d | %d" % (self.bonus.name, self.days, self.price.value)


class PremiumCache(models.Model):
    nick = models.CharField(max_length=512, null=False)
    flags = models.CharField(max_length=512, null=False)
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    time = UnixDateTimeField(null=True, blank=True)
    #user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    premium = models.ForeignKey(
        Premium, on_delete=models.SET_NULL, null=True, blank=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nick

    class Meta:
        db_table = 'shop_premium_cache'
        verbose_name = 'Premium Cache'
        verbose_name_plural = 'Premiums Cache'


class PromotionCode(models.Model):
    code = models.CharField(max_length=512)
    value = models.DecimalField(
        max_digits=19,
        decimal_places=2,
        default=0)
    read_count = models.IntegerField(default=0)
    multi = models.BooleanField(default=False)
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)

    def __str__(self):
        return "%s | %s" % (self.code, self.value)

    class Meta:
        db_table = 'shop_promotion_code'
        verbose_name = 'Kod promocyjny'
        verbose_name_plural = 'Kody promocyjne'

class PromotionServicePrice(models.Model):

    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    percent = models.FloatField(default=0.0)

    def __str__(self):
        return "%.2f" % (self.percent)

    class Meta:
        verbose_name = 'Sklep - Promocyjna cena'
        verbose_name_plural = 'Sklep - Promocyjne ceny'
