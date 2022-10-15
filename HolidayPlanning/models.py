from django.db import models
from datetime import *

class Utente(models.Model):
    nrSocio = models.IntegerField(primary_key=True)#chiave
    nome = models.CharField()
    cognome = models.CharField()
    email = models.CharField()
    #codiceFiscale = models.CharField()
    #telefono = models.CharField()
    #dataDiNascita = models.DateField()

'''classe modello per l'attrazione'''
class Attrazione(models.Model):
    nome = models.CharField(max_length=200, primary_key=True)
    luogo = models.CharField(max_length=300)
    via = models.CharField(max_length=500)
    citta = models.CharField(max_length=200)
    costo = models.FloatField(default=10.5)
    tipo = models.CharField(max_length=200)
    oraApertura = models.DateTimeField('ora apertura')
    oraChiusura = models.DateTimeField('ora chiusura')
    descrizione = models.TextField()
    #def __str__(self):
    #   return  self.__str__(self.nome, self.posizione, self.tipo)

class Scelta(models.Model):
    #TODO chiave è composta dalla chiave di utente e di attrazione e giorno in mezzo
    giorno = models.DateTimeField() #scelto dall'utente
    attrazione = models.ForeignKey('Attrazione')
    oraInizio = models.DateTimeField(blank=True) #scelta dall'utente
    oraFine = models.DateTimeField(blank=True) #scelta dall'utente
    durata = models.DurationField  # questi sono i secondi della durata
    posizioneInGiornata = models.IntegerField() #numero progressivo
    #override del metodo save
    def save(self, *args, **kwargs):
        if(self.controllaOrari(self)):
            self.durata = self.oraFine - self.oraInizio
            # chiamata al vero metodo save
            super(Attrazione, self).save(*args, **kwargs)

    # TODO controllare che ora inizio e fine siano ammissibili
    def controllaOrari(self):
        return True