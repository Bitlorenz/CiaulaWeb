from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.messages.views import SuccessMessageMixin

from profiles.mixins import IsMyselfMixin
from profiles.forms import UserProfileForm, UserUpdateForm
from profiles.models import UserProfileModel


# View per creazione di utente normale
class UserCreateView(SuccessMessageMixin, CreateView):
    model = UserProfileModel
    form_class = UserProfileForm
    template_name = "profiles/user_create.html"
    success_message = "Utente creato correttamente!"
    success_url = reverse_lazy("profiles:user-login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrazione Utente"


# View per aggiornare un nuovo utente, controllando che sia chi fa la richiesta a poterlo fare
class UserUpdateView(SuccessMessageMixin, LoginRequiredMixin, IsMyselfMixin, UpdateView):
    model = UserProfileModel
    form_class = UserUpdateForm
    template_name = 'profiles/update_user.html'
    success_message = 'Utente modificato correttamente!'

    def get_success_url(self):
        return reverse_lazy('profiles:user-detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Modifica Utente"


# view per poter visualizzare tutti i dettagli di un certo utente
class UserDetailView(DetailView):
    model = UserProfileModel
    template_name = 'profiles/user_detail.html'
