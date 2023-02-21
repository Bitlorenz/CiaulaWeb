from django.urls import path, include
from django.contrib import admin
from .views import *

app_name = 'HolidayPlanning'
urlpatterns = [
    path("listaattrazioni/", lista_attrazioni, name="listaattrazioni"),
    path("scegliattr/", crea_scelta_da_citta, name="scegliattr"),
    # es: /HolidayPlanning/cerca/PALERMO/
    path("cerca/<str:attrazione_citta>/", attrazione, name='attrazione'),
    path("attrazioni/", AttrazioniList.as_view(), name="attrazioni"),
    path("scegliattrazione/", ScegliAttrazione.as_view(), name="scegliattrazione"),
]
