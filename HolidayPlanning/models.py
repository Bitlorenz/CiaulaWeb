import datetime

from django.db import models
class Attrazione(models.Model):
    objects = None
    nome = models.CharField(max_length=200, primary_key=True)
    luogo = models.CharField(max_length=300)
    via = models.CharField(max_length=500)
    citta = models.CharField(max_length=200)
    costo = models.FloatField()
    tipo = models.CharField(max_length=200)
    oraApertura = models.DateTimeField('ora apertura')
    oraChiusura = models.DateTimeField('ora chiusura')
    descrizione = models.TextField()
    # def __str__(self):
    #   return  self.__str__(self.nome, self.posizione, self.tipo)

class Scelta(models.Model):
    giorno = models.DateTimeField()  # scelto dall'utente
    attrazione = models.ForeignKey(to='Attrazione', on_delete=models.CASCADE, related_name="attrazione")
    #utente = models.ForeignKey(to=profiles.models.UserProfileModel, related_name='Utente', on_delete=models.CASCADE)
    oraInizio = models.DateTimeField(blank=True)  # scelta dall'utente
    oraFine = models.DateTimeField(blank=True)  # scelta dall'utente
    durata = models.DurationField()  # questi sono i secondi della durata
    posizioneInGiornata = models.IntegerField()  # numero progressivo

    # override del metodo save
    # TODO controllare che ora inizio e fine siano ammissibili

class Giornata(models.Model):
    data = models.DateField()
    numeroGiornata = models.IntegerField()
    totAttrazioni = models.IntegerField()
    totCosto = models.FloatField()
    scelte = models.ManyToManyField(Scelta, related_name='giornate')


class Vacanza(models.Model):
    dataArrivo = models.DateTimeField()
    dataPartenza = models.DateTimeField()
    nrPersone = models.IntegerField()
    budgetDisponibile = models.FloatField()
    totGiorni = models.IntegerField()
    totNotti = models.IntegerField()
    giornata = models.ManyToManyField(Giornata, related_name='vacanze')