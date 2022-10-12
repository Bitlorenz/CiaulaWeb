from django.db import models
from datetime import *
class Attrazione(models.Model):
    nome = models.CharField(max_length=200)
    posizione = models.CharField(max_length=300)
    costo = models.DecimalField(max_digits=4, decimal_places=4, default=10.5)
    durata = models.DurationField#questi sono i minuti
    tipo = models.CharField(max_length=200)
    oraInizio = models.DateTimeField('ora inizio')
    oraFine = models.DateTimeField('ora fine')

    #def __str__(self):
    #   return  self.__str__(self.nome, self.posizione, self.tipo)

    def calcolaDurata(self):
        return self.oraFine - self.oraInizio

class Giornata(models.Model):
    numero = models.IntegerField#TODO chiave
    attrazioni = models.ForeignKey(Attrazione, on_delete=models.CASCADE)
    #attrazioni = models.CharField(max_length=500)#TODO è una lista di attrazioni salvate sul db
    oraSveglia = models.DateTimeField('ora Sveglia')
    oraRientro = models.DateTimeField('Ora Rientro')

    def __str__(self):
        return self.Giornata_text


