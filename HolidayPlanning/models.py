from django.db import models
from datetime import *

class Utente(models.Model):
    nrSocio = models.IntegerField()#chiave
    nome = models.CharField()
    cognome = models.CharField()
    codiceFiscale = models.CharField()
    email = models.CharField()

'''classe modello per l'attrazione'''
class Attrazione(models.Model):
    nome = models.CharField(max_length=200)
    posizione = models.CharField(max_length=300)
    costo = models.FloatField(default=10.5)
    durata = models.DurationField#questi sono i secondi della durata
    tipo = models.CharField(max_length=200)
    oraInizio = models.DateTimeField('ora inizio')#TODO APERTURA
    oraFine = models.DateTimeField('ora fine')#TODO CHIUSURA

    #override del metodo save
    def save(self, *args, **kwargs):
        self.durata = self.oraFine - self.oraInizio
        super(Attrazione, self).save(*args, **kwargs)#chiamata al vero metodo save
    #def __str__(self):
    #   return  self.__str__(self.nome, self.posizione, self.tipo)

class Scelta(models.Model):
    #TODO chiave è composta dalla chiave di utente e di attrazione e giorno in mezzo
    #TODO controllare che ora inizio e fine siano ammissibili
    giorno = models.DateTimeField()
    oraInizio = models.DateTimeField()
    oraFine = models.DateTimeField()
    numero = models.IntegerField()
