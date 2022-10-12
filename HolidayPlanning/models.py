from django.db import models

class Attrazione(models.Model):
    nome = models.CharField(max_length=200)#TODO chiave
    posizione = models.CharField(max_length=300)
    costo = models.FloatField
    durata = models.IntegerField
    tipo = models.CharField(max_length=200)
    oraInizio = models.DateTimeField
    oraFine = models.DateTimeField

class Giornata(models.Model):
    numero = models.IntegerField#TODO chiave
    attrazioni = models.CharField(max_length=500)#TODO è una lista di attrazioni salvate sul db


