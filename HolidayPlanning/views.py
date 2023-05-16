from datetime import timedelta as td

from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm, CreaVacanzaForm, ScegliAttrazioneForm
from .models import Attrazione, Scelta, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


# class view per vedere tutte le attrazioni presenti
class AttrazioniList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/provacbv.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural


# class view per creare una scelta da un elenco di attrazioni
class ScegliOrarioGiornoAttrazione(CreateView):
    model = Scelta
    template_name = "HolidayPlanning/scegli_attrazione.html"
    form_class = ScegliAttrazioneForm
    success_url = reverse_lazy("HolidayPlanning:scelte")

    def get_context_data(self, **kwargs):
        primary_key = self.kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['title'] = primary_key
        return context


    # postprocessing della scelta
    def form_valid(self, form):
        scelta = form.save(commit=False)
        ctx = self.get_context_data()
        primary_key = ctx['title']
        scelta.attrazione = Attrazione.objects.get(pk=primary_key)
        att = scelta.attrazione
        fine = scelta.oraFine
        ini = scelta.oraInizio
        print("oraFine: " + str(fine)+" oraInizio: "+str(ini)+" oraApertura attrazione: "+str(scelta.attrazione.oraApertura))
        scelta.durata = td(hours=fine.hour - ini.hour)+td(minutes=fine.minute-ini.minute)
        creatore_scelta = self.request.user
        rifvacanza = Vacanza.objects.filter(utente=creatore_scelta).last()
        if not (scelta.attrazione.oraApertura < ini < scelta.attrazione.oraChiusura
                and scelta.attrazione.oraApertura < fine < scelta.attrazione.oraChiusura):
            print("ORARI NON AMMISSIBILI")
            form.add_error("oraInizio", "Inserire orario compreso tra: "+str(att.oraApertura)+" e "+str(att.oraChiusura))
            form.add_error("oraFine", "Inserire orario compreso tra: " + str(att.oraApertura)+" e "+str(att.oraChiusura))
            # elif not rifvacanza.dataArrivo < scelta.giorno < rifvacanza.dataPartenza:
            #    form.add_error("giorno", "Inserire giorno tra "+str(rifvacanza.dataArrivo)+" e "+str(rifvacanza.dataPartenza))
            # elif self.checkSovrapposizione(self, fine, ini):
            #    form.add_error("oraInizio", "Sovrapposizione con altre scelte")
        else:
            scelta.save()
            rifvacanza.scelte.add(scelta)
            return super().form_valid(form)

def get_success_url(self):
    ctx = self.get_context_data()
    pk = ctx["object"].pk
    return reverse("HolidayPlanning:dettaglioscelta", kwargs={"pk": pk})

def checkSovrapposizione(self, fine, ini):
    creatore_scelta = self.request.user
    rifvacanza = Vacanza.objects.filter(utente=creatore_scelta).last()
    scelteFatte = rifvacanza.scelte
    for i in scelteFatte:
        if i.oraInizio < ini and fine < i.oraFine: # sovrapposizione totale
            return True
        if i.oraInizio < ini < i.oraFine or i.oraInizio < fine < i.oraFine: # sovrapposizione parziale
            return True
    return False



# class view per iniziare a creare una vacanza
class CreaVacanza(LoginRequiredMixin, CreateView):
    model = Vacanza
    form_class = CreaVacanzaForm
    template_name = "HolidayPlanning/crea_vacanza.html"
    success_url = reverse_lazy("HolidayPlanning:attrazioni")

    #def get_context_data(self, **kwargs):
    #    ctx = super().get_context_data(**kwargs)
    #    c = ctx["object"]

    def form_valid(self, form):
        vacanza = form.save(commit=False)
        vacanza.utente = self.request.user
        vacanza.save()
        return super().form_valid(form)


class ScelteList(ListView):
    model = Scelta
    template_name = "HolidayPlanning/listascelte.html"

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Attrazioni Scelte"
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


# function view per vedere tutte le attrazioni presenti
class AttrazioniHome(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/listaattrazioni.html"
    ctx = {"title": "lista di attrazioni", "listaattrazioni": Attrazione.objects.all()}
    # return render(request, template_name=template, context=ctx)


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
