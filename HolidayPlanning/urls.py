from django.urls import path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

app_name = 'HolidayPlanning'
urlpatterns = [
    path("listaattrazioni/", AttrazioniHome.as_view(), name="listaattrazioni"),
    path("attrazioni/", AttrazioniList.as_view(), name="attrazioni"),
    path("scegliattrazione/<pk>", scegliattrazione, name="scegli"),
    path("listascelte/", ScelteList.as_view(), name="scelte"),
    path("detscelta/<pk>", DetailSceltaEntita.as_view(), name="dettaglioscelta"),
    path("attrazioni/detattrazione/<pk>/", DetailAttrazioneEntita.as_view(), name="dettaglioattr"),
    path("editscelta/<pk>/", ModificaScelta.as_view(), name="modificascelta"),
    path("cancellascelta/<pk>", CancellaScelta.as_view(), name="cancellascelta"),
    path("cerca/", cerca, name="cerca"),
    path("risultati/<str:stringa>/<str:where>/", RisultatiList.as_view(), name="risultati"),
    path("sceltafatta/<pk>/", SceltaFattaView.as_view(), name="sceltafatta"),
    path("creavacanza/", CreaVacanza.as_view(), name="creavacanza"),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
