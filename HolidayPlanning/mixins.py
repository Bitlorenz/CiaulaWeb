from django.contrib.auth.mixins import LoginRequiredMixin
from HolidayPlanning.models import Vacanza


# mixin per permettere anche ai non turisti di vedere i tour organizzati
class LookingTourMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        vacanza = Vacanza.objects.get(pk=kwargs['pk'])
        if not request.user.is_authenticated: #se l'utente è anonimo
            if not vacanza.utente.pk == 1:  # se il creatore della vacanza non è root (non è un tour organizzato)
                return self.handle_no_permission() # allora lo buttiamo fuori
        return super().dispatch(request, *args, **kwargs)
