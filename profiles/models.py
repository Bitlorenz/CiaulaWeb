from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django.db.transaction import on_commit
#https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Utenti devono inserire email')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        print("utente salvato tramite profiles.forms.UserManager.create_user")
        user.save(using=self.db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # extra_fields.setdefault('is_staff', True)
        # extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        # user = self.create_user(email, password=password, **extra_fields)
        # user.is_admin = True
        # user.save(using=self.db)
        # return user
        return self.create_user(email, password=password, **extra_fields)


class UserProfileModel(AbstractBaseUser):
    nrSocio = models.IntegerField(primary_key=True)  # chiave, deve autogenerarsi
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=32, unique=True)
    codiceFiscale = models.CharField(max_length=18)
    telefono = models.CharField(max_length=32)
    dataDiNascita = models.DateField(null=True)
    profile_image = models.ImageField(blank=True, null=True, default="defaultuser.png")
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        return self.is_admin

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
