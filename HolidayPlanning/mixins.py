from django.contrib.auth.mixins import LoginRequiredMixin

from HolidayPlanning.models import Vacanza


# mixin per permettere anche ai non turisti di vedere i tour organizzati
class LookingTourMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get('pk')
        if pk != 0:
            print("primary key vacanza nel mixin: "+kwargs['pk'])
        else:
            vacanza = Vacanza.objects.get(pk=kwargs['pk'])
            if not request.user.is_authenticated:
                if not vacanza.utente.pk == 1:  # se il creatore della vacanza non è root allora lo buttiamo fuori
                    return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
