from django.urls import path
from .views import *

app_name = 'HolidayPlanning'
urlpatterns = [
    path("scegliattrazione/<pk>/<vacanza_id>", scegliattrazione, name="aggiungi"),  # pk è dell'attrazione
    path("editscelta/<att_pk>/<pk>/", ModificaScelta.as_view(), name="modificascelta"),
    path("cancellascelta/<att_pk>/<pk>", CancellaScelta.as_view(), name="cancellascelta"),
    path("spostamento/<par>/<pk>", AggiungiSpostamento.as_view(), name="spostamento"),
    path("editspostamento/<pk>/", ModificaSpostamento.as_view(), name="modificaspostamento"),
    path("cancellaspostamento/<pk>", CancellaSpostamento.as_view(), name="cancellaspostamento"),
    path("creavacanza/", CreaVacanza.as_view(), name="creavacanza"),
    path("aggiungitour/<int:pk>", AggiungiTourVacanza.as_view(), name="aggiungitour"),
    path("vacanze/", VacanzeList.as_view(), name="vacanze"),
    path("vacanza/<int:pk>/", DettaglioVacanza.as_view(), name="dettagliovacanza"),
    path("vacanza/<pk>/modificavacanza/", ModificaVacanza.as_view(), name="modificavacanza"),
    path("vacanza/<pk>/stampavacanza/", stampaVacanza, name="stampavacanza"),
    path("tour/", vacanze_by_root, name="tourorganizzati"),
    path("dettour/<int:pk>", TourDetail.as_view(), name="dettagliotour")
    ]
