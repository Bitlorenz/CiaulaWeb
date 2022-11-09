from django.http import HttpResponse
from django.shortcuts import render
from .models import Attrazione

# Create your views here.

def index(request):
    return HttpResponse("Questa è la view della parte in cui si organizza la vacanza")

def lista_attrazioni(request):
    templ = "HolidayPlanning/listaattrazioni.html"

    ctx = { "title":"lista di attrazioni",
            "listaattrazioni" : Attrazione.objects.all()}

    return render(request, template_name=templ, context=ctx)

TIPO_GASTRONOMIA = "gastronomia"
def gastronomia(request):
    templ = "HolidayPlanning/listaattrazioni.html"

    lista_filtrata = Attrazione.objects.filter(tipo__iexact='gastronomia')

    ctx = {"title": "lista di attrazioni gastronomiche",
           "listaattrazioni": lista_filtrata}

    return render(request, template_name=templ, context=ctx)


def attrazione(request, nome_attrazione):
    return HttpResponse("Stai guardando l'attrazione %s." %nome_attrazione)
