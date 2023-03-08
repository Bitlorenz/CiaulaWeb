from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView

from profiles.forms import UserProfileForm
from profiles.models import UserProfileModel


# Create your views here.
class UserCreateView(CreateView):
    #form_class = UserCreationForm
    model = UserProfileModel
    form_class = UserProfileForm
    template_name = "profiles/create_user.html"
    success_message = "Utente creato correttamente!"
    success_url = reverse_lazy("login")

class ManagerCreateView(PermissionRequiredMixin, UserCreateView):
    permission_required = "is_staff"
    form_class = ManagerProfileForm