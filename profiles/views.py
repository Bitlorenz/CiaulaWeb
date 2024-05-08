from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, UpdateView

from profiles.forms import UserCreationForm, UserChangeForm
from profiles.mixins import IsSameUserMixin
from profiles.models import UserProfileModel


# View per creazione di utente normale
class UserCreateView(CreateView):
    model = UserProfileModel
    form_class = UserCreationForm
    template_name = "profiles/user_create.html"
    success_message = "Utente creato correttamente!"
    success_url = reverse_lazy("profiles:user-login")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Registrazione Utente"


# view per poter visualizzare tutti i dettagli di un certo utente
class UserDetailView(DetailView, IsSameUserMixin):
    model = UserProfileModel
    template_name = 'profiles/user_detail.html'


class UserUpdateView(IsSameUserMixin, LoginRequiredMixin, UpdateView):
    model = UserProfileModel
    form_class = UserChangeForm
    template_name = 'profiles/user_update.html'

    def get_success_url(self):
        return reverse_lazy('profiles:user-detail', kwargs={'pk': self.kwargs['pk']})
