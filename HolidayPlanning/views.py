from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse

from .forms import SearchForm
from .models import Attrazione, Scelta
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
