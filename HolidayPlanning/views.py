from datetime import timedelta as td

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm, CreaVacanzaForm, ScegliAttrazioneForm
from .models import Attrazione, Scelta, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


# class view per vedere tutte le attrazioni presenti
class AttrazioniList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/attrazionilista.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['listaattrazioni'] = Attrazione.objects.all()
        utente = self.request.user
        context['user'] = utente
        return context


def scegliattrazione(request, pk):
    if request.method == "POST":
        form = ScegliAttrazioneForm(data=request.POST, pk=pk, user=request.user)
        if form.is_valid():
            scelta = form.save(commit=False)
            rifvacanza = Vacanza.objects.filter(utente=request.user).last()
            ini = form.cleaned_data.get("oraInizio")
            fine = form.cleaned_data.get("oraFine")
            scelta.durata = td(hours=fine.hour - ini.hour) + td(minutes=fine.minute - ini.minute)
            #checkSovrapposizione(request, fine, ini)
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return redirect("HolidayPlanning:dettaglioscelta", scelta.pk)
    else:
        utente = request.user
        att = get_object_or_404(Attrazione, pk=pk)
        form = ScegliAttrazioneForm(pk=pk, user=utente)
        #TODO CONTROLLARE SE ESISTE UNA VACANZA PER L'UTENTE, SE NO CREARNE UNA
        if (Vacanza.objects.filter(utente=utente).count() == 0):
            return redirect("HolidayPlanning:creavacanza")
        return render(request, template_name="HolidayPlanning/scegli_attrazione.html", context={"form": form, "att": att, "title": att.nome})
    return render(request, template_name="HolidayPlanning/scegli_attrazione.html", context={"form": form})

#TODO non ritornare T/F, ma stampare un messaggio avvertendo che c'è sovrapposizione con la specifica scelta
def checkSovrapposizione(request, fine, ini):
    rifvacanza = Vacanza.objects.filter(utente=request.user).last()
    scelteFatte = rifvacanza.scelte
    for i in scelteFatte:
        if i.oraInizio < ini and fine < i.oraFine: # sovrapposizione totale
            sovrapposta = i
        if i.oraInizio < ini < i.oraFine or i.oraInizio < fine < i.oraFine: # sovrapposizione parziale
            return True
    return False


# class view per iniziare a creare una vacanza
class CreaVacanza(LoginRequiredMixin, CreateView):
    model = Vacanza
    form_class = CreaVacanzaForm
    template_name = "HolidayPlanning/crea_vacanza.html"
    success_url = reverse_lazy("HolidayPlanning:attrazioni")

    def form_valid(self, form):
        vacanza = form.save(commit=False)
        vacanza.utente = self.request.user
        vacanza.save()
        return super().form_valid(form)


class ScelteList(LoginRequiredMixin, ListView):
    model = Scelta
    template_name = "HolidayPlanning/listascelte.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Itinerario di Viaggio"
        context['utente'] = self.request.user
        context['vacanzacorrente'] = Vacanza.objects.filter(utente=self.request.user).last()
        #context['scelte'] = Scelta.objects.filter(utente=self.request.user)
        context['scelte'] = context['vacanzacorrente'].scelte.all()
        return context


# class detail view per una scelta
class DetailSceltaEntita(DetailView):
    model = Scelta
    template_name = "HolidayPlanning/dettaglioscelta.html"


# class detail view per un'attrazione
class DetailAttrazioneEntita(DetailView):
    model = Attrazione
    template_name = "HolidayPlanning/dettaglioattrazione.html"


# class per modificare una scelta data la chiave primaria
class ModificaScelta(UpdateView):
    model = Scelta
    template_name = "HolidayPlanning/modificascelta.html"
    fields = ['giorno', 'oraInizio', 'oraFine']

    def get_success_url(self):
        # pk = self.get_context_data()["object"].pk
        return reverse("HolidayPlanning:dettaglioscelta") # , kwargs={'pk': id})


# class delete view per eliminare una scelta
class CancellaScelta(DeleteView):
    model = Scelta
    template_name = "HolidayPlanning/cancellascelta.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        entita = "Scelta"
        ctx["entita"] = entita
        return ctx

    def get_success_url(self):
        return reverse("HolidayPlanning:scelte")


# ##FORMS###
# raggiunta tramite richiesta GET, al click del pulsante submit, i dati inseriti (nei campi definiti dal SearchForm)
# re-indirizzeranno sul secondo url, i cui parametri sono compilati in funzione di request.POST
def cerca(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            stringa = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")  # indica la table su cui vogliamo fare la query
            return redirect("HolidayPlanning:risultati", stringa, where)
    else:
        form = SearchForm()  # è il form personalizzato, passato poi in context

    return render(request, template_name="HolidayPlanning/cerca.html", context={"form": form})


class RisultatiList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/risultati.html"

    def get_queryset(self):
        stringa = self.request.resolver_match.kwargs["stringa"]
        where = self.request.resolver_match.kwargs["where"]

        if "Scelta" in where:
            sc = Scelta.objects.filter(posizioneInGiornata__exact=int(stringa))
            return sc
        if "Attrazione" in where:
            sa = Attrazione.objects.filter(citta__icontains=stringa)
            return sa


class SceltaFattaView(LoginRequiredMixin, DetailView):
    model = Scelta
    template_name = "HolidayPlanning/sceltafatta.html"
    errore = "NO_ERRORS"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        c = ctx["object"]

        if c.giorno != None:
            if c.utente.pk != self.request.user.pk:
                self.errore = "Non hai scelto attività per questo giorno"
        else:
            self.errore = "Attività ancora non scelta"

        if self.errore == "NO_ERRORS":
            try:
                c.giorno = None
                c.utente = None
                c.save()
            except Exception as e:
                print("Errore! " + str(e))
                self.errore = "Errore nell'operazione di restituzione"

        return ctx
