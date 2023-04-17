from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SearchForm, CreaVacanzaForm
from .models import Attrazione, Scelta, Vacanza
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


# class view per vedere tutte le attrazioni presenti
class AttrazioniList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/provacbv.html"

    # paginate_by = 10
    def get_queryset(self):
        return self.model.objects.exclude(costo__exact=0)

    def get_model_name(self):
        return self.model._meta.verbose_name_plural

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titolo'] = "Attrazioni non gratuite"
        return context


# class view per creare una scelta da un elenco di attrazioni
class ScegliAttrazione(CreateView):
    model = Scelta
    template_name = "HolidayPlanning/scegli_attrazione.html"
    fields = "__all__"
    success_url = reverse_lazy("HolidayPlanning:scelte")


# class view per iniziare a creare una vacanza
class CreaVacanza(CreateView):
    model = Vacanza
    form_class = CreaVacanzaForm
    template_name = "HolidayPlanning/crea_vacanza.html"
    #success_message = "Vacanza creata correttamente"
    success_url = reverse_lazy("HolidayPlanning:scegliattrazione")

    def form_valid(self, form):
        #campi per attribuire l'appartenenza della vacanza ad un utente
        #form.instance.creatore_vacanza = self.request.user
        return super().form_valid(form)

# class view per vedere tutte le scelte presenti
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
        pk = self.get_context_data()["object"].pk
        return reverse("HolidayPlanning:dettaglioscelta", kwargs={'pk': pk})


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
@login_required
def lista_attrazioni(request):
    template = "HolidayPlanning/listaattrazioni.html"
    ctx = {"title": "lista di attrazioni", "listaattrazioni": Attrazione.objects.all()}
    return render(request, template_name=template, context=ctx)


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
