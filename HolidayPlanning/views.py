import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse

from .models import Attrazione, Scelta
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView


# Create your views here.

def crea_scelta_da_citta(request):
    message = ""

    if "citta" in request.GET and "luogo" in request.GET:
        cittaScelta = request.GET["citta"]
        # luogoScelta = request.GET["luogo"]
        print("Citta inserita: " + cittaScelta)
        # print("luogo inserito: " + luogoScelta)
        posizioneInGiornata = 0

        try:
            posizioneInGiornata = int(request.GET["posizioneInGiornata"])
        except Exception as e:
            message = "Posizione non valida. Inserita posizione di default." + str(e)

        att = get_object_or_404(Attrazione, citta=cittaScelta)
        print(att.nome)
        s = Scelta()
        s.giorno = datetime.date(2023, 6, 12)
        s.attrazione = att
        s.oraInizio = datetime.time(20)
        s.oraFine = datetime.time(22, 30)
        s.durata = datetime.timedelta(hours=s.oraFine.hour - s.oraInizio.hour,
                                      minutes=s.oraFine.minute - s.oraInizio.minute)
        s.posizioneInGiornata = posizioneInGiornata

        try:
            s.save()
            message = "Creazione Scelta riuscita!" + message
        except Exception as e:
            message = "Errore nella creazione della Scelta " + str(e)

    return render(request, template_name="HolidayPlanning/scegliattr.html",
                  context={"title": "Scegli Attrazione", "message": message})


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

#class detail view per una scelta
class DetailSceltaEntita(DetailView):
    model = Scelta
    template_name = "HolidayPlanning/dettaglioscelta.html"

#class detail view per un'attrazione
class DetailAttrazioneEntita(DetailView):
    model = Attrazione
    template_name = "HolidayPlanning/dettaglioattrazione.html"


#class per modificare una scelta data la chiave primaria
class ModificaScelta(UpdateView):
    model = Scelta
    template_name = "HolidayPlanning/modificascelta.html"
    fields = ['giorno', 'oraInizio', 'oraFine']

    def get_success_url(self):
        pk = self.get_context_data()["object"].pk
        return reverse("HolidayPlanning:dettaglioscelta", kwargs={'pk': pk})


#class delete view per eliminare una scelta
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
