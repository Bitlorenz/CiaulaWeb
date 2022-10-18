from django.db import models
from django.contrib.auth.models import User, AbstractUser
#from django.db.transaction import on_commit
#https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms

class UserProfileModel(AbstractUser):
    nrSocio = models.IntegerField(primary_key=True)  # chiave, deve autogenerarsi
    nome = models.CharField()
    cognome = models.CharField()
    email = models.CharField()
    codiceFiscale = models.CharField()
    telefono = models.CharField()
    dataDiNascita = models.DateField()
