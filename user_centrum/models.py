from django.db import models
from servers.models import Server
from accounts.models import User

# Podanie
class Application(models.Model):
    ADMIN = 'Admin'
    JUNIOR_ADMIN = 'Junior Admin'
    TYPE_CHOICES = (
        (ADMIN, 'Admin'),
        (JUNIOR_ADMIN, 'Junior Admin')
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=50, verbose_name='Typ podania', choices=TYPE_CHOICES, default=ADMIN)
    server = models.ForeignKey(Server, verbose_name='Serwer', on_delete=models.CASCADE)
    name = models.CharField(max_length=50, verbose_name='Imie')
    age = models.PositiveIntegerField(verbose_name='Wiek')
    microphone = models.BooleanField(default=False, verbose_name='Mikrofon')
    reason = models.TextField(verbose_name='Powod')
    experiance = models.TextField(verbose_name='Doswiadczenie')
    created = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Podanie'
        verbose_name_plural = 'Podania'
        permissions = (
            ('accept_application', 'Może aktywować podania'),
            ('cancel_application', 'Może odrzucac podania')
        )

    def have_micro(self):
        if self.microphone:
            return 'Tak'
        else:
            return 'Nie'
    
    def accept(self):
        self.status = 1
        return self.save()

    def cancel(self):
        self.status = -1
        return self.save()

#Komentarz do podania
class ApplicationComments(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(verbose_name='Treść')
    created = models.DateTimeField(auto_now_add=True)
    owner_name = models.CharField(max_length=50, null=True)
    owner_avatar = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.content

    class Meta:
        verbose_name = 'Podanie - komentarz'
        verbose_name_plural = 'Podanie - komentarze'

