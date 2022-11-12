from django.urls import path, include
from django.contrib import admin
from . import views
from .views import lista_attrazioni, crea_scelta_da_citta

urlpatterns = [
    path('', views.index, name='index'),
    path("listaattrazioni/",lista_attrazioni, name="listaattrazioni"),
    path("scegliattr/", crea_scelta_da_citta, name="scegliattr")
]