from django.urls import path, include
from django.contrib import admin
from .views import *

app_name = 'HolidayPlanning'
urlpatterns = [
    path("listaattrazioni/", lista_attrazioni, name="listaattrazioni"),
    path("scegliattr/", crea_scelta_da_citta, name="scegliattr"),
    path("attrazioni/", AttrazioniList.as_view(), name="attrazioni"),
    path("scegliattrazione/", ScegliAttrazione.as_view(), name="scegliattrazione"),
    path("listascelte/", ScelteList.as_view(), name="scelte"),
    path("detscelta/<pk>/", DetailSceltaEntita.as_view(), name="dettaglioscelta"),
    path("detattrazione/<pk>/", DetailAttrazioneEntita.as_view(), name="dettaglioattr"),
    path("editscelta/<pk>/", ModificaScelta.as_view(), name="modificascelta"),
    path("cancellascelta/<pk>", CancellaScelta.as_view(), name="cancellascelta"),
]
