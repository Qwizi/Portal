from django.db import models
from servers.models import Server
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

class Rule(models.Model):
    server = models.ForeignKey(Server, on_delete=models.CASCADE)
    content = models.TextField(_('Treść'))
    is_active = models.BooleanField(_('Jest aktywny?'), default=True)

    def __str__(self):
        return self.server.name

    def get_absolute_url(self):
        return reverse('mainpage_rules_detail', kwargs={'server': self.server.tag})

    class Meta:
        verbose_name = 'Regulamin'
        verbose_name_plural = 'Regulaminy'

class FAQ(models.Model):
    question = models.CharField(_('Pytanie'), max_length=255)
    answer = models.TextField(_('Odpowiedź'))
    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Faq'
        verbose_name_plural = 'Faqs'