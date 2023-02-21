import datetime

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.urls import reverse_lazy

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


def modscelta(request, scelta_da_modificare=None):
    msg = ""
    title = "Modifica Libro"
    templ = "HolidayPlanning/modificascelta.html"  # TODO fare il template
    # modifica libro
    if "citta" in request.GET:
        inizioH = datetime.time(hour=11)
        fineH = datetime.time(hour=12)
        try:
            inizioH = datetime.time(hour=int(request.GET["inizioH"]))
            fineH = datetime.time(hour=int(request.GET["fineH"]))
        except Exception as e:
            msg = " Orari imposti al default" + str(e)

        scelta_da_modificare.oraInizio = inizioH
        scelta_da_modificare.oraFine = fineH

        try:
            scelta_da_modificare.save()
            msg = "Aggiornamento completato! " + msg
        except Exception as e:
            msg = "Errore nella modifica della scelta " + str(e)

    ctx = {"title": title, "scelta": scelta_da_modificare, "message": msg}
    return render(request, template_name=templ, context=ctx)


def modifica_scelta(request, InCitta):
    sce = get_object_or_404(Scelta, citta=InCitta)
    return modscelta(request, sce)


# class view per vedere tutte le attrazioni presenti
class AttrazioniList(ListView):
    model = Attrazione
    template_name = "HolidayPlanning/provacbv.html"
    #paginate_by = 10
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
    success_url = reverse_lazy("HolidayPlanning:listaattrazioni")

# function view per vedere tutte le attrazioni presenti
def lista_attrazioni(request):
    template = "HolidayPlanning/listaattrazioni.html"
    ctx = {"title": "lista di attrazioni", "listaattrazioni": Attrazione.objects.all()}
    return render(request, template_name=template, context=ctx)


# function view di prova che stampa a schermo il parametro passato come nome_attrazione
def attrazione(request, attrazione_citta):
    attrazionevar = get_list_or_404(Attrazione, citta__iexact=attrazione_citta)
    print(attrazionevar)
    context = {"title": "Attrazione da citta", 'attrazione': attrazionevar}
    return render(request, 'HolidayPlanning/attrazione.html', context)
