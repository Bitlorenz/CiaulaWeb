from django.urls import path
from .views import *

app_name = 'HolidayPlanning'
urlpatterns = [
    path("scegliattrazione/<pk>/<vacanza_id>", scegliattrazione, name="scegli"),  # la prima pk è dell'attrazione la seconda della vacanza
    path("listascelte/<int:pk>", ScelteList.as_view(), name="scelte"),
    path("editscelta/<pk>/", ModificaScelta.as_view(), name="modificascelta"),
    path("cancellascelta/<pk>", CancellaScelta.as_view(), name="cancellascelta"),
    path("spostamento/<par>/<arr>", AggiungiSpostamento.as_view(), name="spostamento"),
    # path("risultati/<str:stringa>/<str:where>/", RisultatiList.as_view(), name="risultati"),
    path("sceltafatta/<pk>/", SceltaFattaView.as_view(), name="sceltafatta"),
    path("creavacanza/", CreaVacanza.as_view(), name="creavacanza"),
    path("aggiungitour/<int:pk>", AggiungiTourVacanza.as_view(), name="aggiungitour"),
    path("vacanze/", VacanzeList.as_view(), name="vacanze"),
    path("vacanza/<pk>/", DettaglioVacanza.as_view(), name="dettagliovacanza"),
    path("vacanza/<pk>/modificavacanza/", ModificaVacanza.as_view(), name="modificavacanza"),
    path("vacanza/<pk>/stampavacanza/", stampaVacanza, name="stampavacanza"),
    path("tour/", vacanze_by_root, name="tourorganizzati"),
    ]
