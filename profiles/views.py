from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView

from profiles.forms import UserCreationForm
from profiles.models import UserProfileModel


# View per creazione di utente normale
class UserCreateView(CreateView):
    print("chiamata la view profiles.view.UserCreateView")
    model = UserProfileModel
    #fields = ('first_name',)
    form_class = UserCreationForm
    template_name = "profiles/user_create.html"
    success_message = "Utente creato correttamente!"
    success_url = reverse_lazy("profiles:user-login")


# view per aggiornare un profilo utente
# class UserUpdateView(UpdateView):

