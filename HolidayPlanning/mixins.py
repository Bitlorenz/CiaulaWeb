from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, get_object_or_404

from HolidayPlanning.models import Vacanza


# mixin per permettere anche ai non turisti di vedere i tour organizzati
class LookingTourMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)

        if pk is not None:
            if request.user.is_authenticated:
                # Redirect authenticated users to their last vacation if pk is not specified
                last_vacation = Vacanza.objects.filter(utente=request.user).last()
                if last_vacation:
                    self.kwargs['pk'] = last_vacation.pk
            else:
                # For anonymous users, allow access only if the creator of the vacation is the root user
                vacation = get_object_or_404(Vacanza, pk=pk)
                if vacation.utente.pk != 1:
                    return self.handle_no_permission()

        return super().dispatch(request, *args, **kwargs)
    '''
    def dispatch(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk",0)
        if pk is not None:
            if request.user.is_authenticated:
                self.kwargs['pk'] = Vacanza.objects.filter(utente=self.request.user).last().id
                return super().dispatch(request, *args, **kwargs)
            else: #è un utente anonimo che vuole vedere un tour organizzato
                vacanza = Vacanza.objects.get(pk=kwargs['pk'])
                if vacanza.utente.pk == 1:
                    print("utente non autenticato vuole vedere tour organizzato")
                    return super().dispatch(request, *args, **kwargs)
        else:
            vacanza = Vacanza.objects.get(pk=kwargs['pk'])
            if not request.user.is_authenticated:
                if not vacanza.utente.pk == 1:  # se il creatore della vacanza non è root allora lo buttiamo fuori
                    return self.handle_no_permission()
            return super().dispatch(request, *args, **kwargs)
    '''