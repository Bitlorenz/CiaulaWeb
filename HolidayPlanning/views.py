import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Attrazione, Scelta
from django.db.models import CharField
from django.db.models.functions import Cast


# Create your views here.


def index():
    return HttpResponse("Questa è la view della parte in cui si organizza la vacanza")


def crea_scelta_da_citta(request):
    message = ""

    if "citta" in request.GET and "luogo" in request.GET:
        cittaScelta = request.GET["citta"]
        luogoScelta = request.GET["luogo"]
        print("Citta inserita: "+cittaScelta)
        print("luogo inserito: "+luogoScelta)
        posizioneInGiornata = 0

        try:
            posizioneInGiornata = int(request.GET["posizioneInGiornata"])
        except:
            message = "Posizione non valida. Inserita posizione di default."

        att = get_object_or_404(Attrazione, citta=cittaScelta, luogo=luogoScelta)
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


def lista_attrazioni(request):
    templ = "HolidayPlanning/listaattrazioni.html"

    ctx = {"title": "lista di attrazioni",
           "listaattrazioni": Attrazione.objects.all()}

    return render(request, template_name=templ, context=ctx)


TIPO_GASTRONOMIA = "gastronomia"


def gastronomia(request):
    templ = "HolidayPlanning/listaattrazioni.html"

    lista_filtrata = Attrazione.objects.filter(tipo__iexact='gastronomia')

    ctx = {"title": "lista di attrazioni gastronomiche",
           "listaattrazioni": lista_filtrata}

    return render(request, template_name=templ, context=ctx)


def attrazione(nome_attrazione):
    return HttpResponse("Stai guardando l'attrazione %s." % nome_attrazione)
