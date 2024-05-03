from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404

from HolidayPlanning.models import Vacanza


# mixin per permettere anche ai non turisti di vedere i tour organizzati
# e non permette di guardare la vacanza di un altro utente
class LookingTourMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        vacanza = Vacanza.objects.get(pk=kwargs['pk'])
        if not request.user.is_authenticated:  # se l'utente è anonimo
            if not vacanza.utente.pk == 1:  # se il creatore della vacanza non è root (non è un tour organizzato)
                return self.handle_no_permission()  # allora lo buttiamo fuori
        if request.user != vacanza.utente:
            raise Http404("Non hai il permesso per accedere a questa vacanza.")
        return super().dispatch(request, *args, **kwargs)


# Mixin per assicurarsi che l'oggetto (vacanza) cui si accede appartiene all'utente che lo richiede.
class IsVacanzaUserOwnedMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        vacanza = Vacanza.objects.get(pk=kwargs['pk'])
        if vacanza.utente != request.user:
            raise Http404("Non hai il permesso per accedere a questa vacanza.")
        return super().dispatch(request, *args, **kwargs)


