from django.db import models
from django.contrib.auth.models import User, AbstractUser
#from django.db.transaction import on_commit
#https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms

class UserProfileModel(AbstractUser):
    nrSocio = models.IntegerField(primary_key=True)  # chiave, deve autogenerarsi
    nome = models.CharField(max_length=32)
    cognome = models.CharField(max_length=32)
    email = models.CharField(max_length=32)
    codiceFiscale = models.CharField(max_length=18)
    telefono = models.CharField(max_length=32)
    dataDiNascita = models.DateField()

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
