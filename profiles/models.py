from django.db import models
from django.contrib.auth.models import User, AbstractBaseUser
# https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms


#class UserManager(BaseUserManager):
    #use_in_migrations = True

    #def create_user(self, email, password=None, **extra_fields):
        #if not email:
        #    raise ValueError('Utenti devono inserire email')
        #email = self.normalize_email(email)
        #user = self.model(email=email, **extra_fields)
        #user.set_password(password)
        #print("utente salvato tramite profiles.forms.UserManager.create_user")
        #user.save(using=self.db)
        #return user

    #def create_superuser(self, email, password=None, **extra_fields):
        #extra_fields.setdefault('is_active', True)
        #extra_fields.setdefault('is_admin', True)
        #return self.create_user(email, password=password, **extra_fields)


class UserProfileModel(AbstractBaseUser):
    nrSocio = models.IntegerField(primary_key=True)
    first_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    email = models.CharField(max_length=32, unique=True)
    codiceFiscale = models.CharField(max_length=18, blank=True, null=True)
    telefono = models.CharField(max_length=15)
    dataDiNascita = models.DateField(null=True)
    profile_image = models.ImageField(blank=True, null=True, default="defaultuser.png", upload_to="profiles/photos")
    is_admin = models.BooleanField(default=False)

    # objects = UserManager()
    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = []

    def __str__(self):
        return "Utente: "+self.first_name+" "+self.last_name+", "+str(self.email)

    @property
    def is_staff(self):
        return self.is_admin

    #def has_module_perms(self):
    #    return True

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
