from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView

from profiles.forms import UserProfileForm, ManagerProfileForm
from profiles.models import UserProfileModel


# View per creazione di utente normale
class UserCreateView(CreateView):
    #form_class = UserCreationForm
    model = UserProfileModel
    form_class = UserProfileForm
    template_name = "profiles/create_user.html"
    success_message = "Utente creato correttamente!"
    success_url = reverse_lazy("login")


# view per aggiornare un profilo utente
#class UserUpdateView(UpdateView):


# view per creazione utente staff, tour manager, può aggiungere attività
class ManagerCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = ManagerProfileForm