from django.urls import path
from .views import *

app_name = 'attractions'
urlpatterns = [
    #  url per la visualizzazione di più attrazioni
    path("attrazioni/", AttrazioniList.as_view(), name="attrazioni"),
    #  url per mostrare i dettagli di un attrazione
    path("attrazioni/detattrazione/<str:nome_attr>", DetailAttrazioneEntita, name="dettaglioattr"), #LASCIARE nome_attr
    #  url per cercare un attrazione
    path("cerca/", SearchView.as_view(), name="cerca"),
    #  Url per l'aggiunta di un'attrazione da parte dell'admin
    path("creaattrazione/", AttrazioneCreateView.as_view(), name="crea_attrazione"),
    #  Url per la modifica di un attrazione da parte dell'admin
    path("modificaattrazione/<pk>", AggiornaAttrazione.as_view(), name="modifica_attrazione"),
    # url per l'inserimento di una recensione per un'attrazione scelta
    path("recensione/<str:pk>", RecensioneCreateView.as_view(), name="crea_recensione")
]
