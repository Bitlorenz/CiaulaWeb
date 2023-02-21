from django.db import models


class Attrazione(models.Model):
    objects = None
    nome = models.CharField(max_length=200, primary_key=True)
    luogo = models.CharField(max_length=300)
    via = models.CharField(max_length=500)
    citta = models.CharField(max_length=200)
    costo = models.FloatField()
    tipo = models.CharField(max_length=200)
    oraApertura = models.TimeField('ora apertura')
    oraChiusura = models.TimeField('ora chiusura')
    descrizione = models.TextField()

    def __str__(self):
        return "ID: " + str(self.pk) + ": " + self.nome + " di tipo " + self.tipo + " a " + self.citta

    class Meta:
        verbose_name_plural = "Attrazioni"


class Scelta(models.Model):
    giorno = models.DateField()  # scelto dall'utente
    attrazione = models.ForeignKey(to='Attrazione', on_delete=models.CASCADE, related_name="attrazione")
    # utente = models.ForeignKey(to=profiles.models.UserProfileModel, related_name='Utente', on_delete=models.CASCADE)
    oraInizio = models.TimeField(blank=True)  # scelta dall'utente
    oraFine = models.TimeField(blank=True)  # scelta dall'utente
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
    dataArrivo = models.DateField()
    dataPartenza = models.DateField()
    nrPersone = models.IntegerField()
    budgetDisponibile = models.FloatField()
    totGiorni = models.IntegerField()
    totNotti = models.IntegerField()
    giornata = models.ManyToManyField(Giornata, related_name='vacanze')
