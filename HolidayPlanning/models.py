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
        verbose_name = "Attrazione"
        verbose_name_plural = "Attrazioni"


class Scelta(models.Model):
    giorno = models.DateField()  # scelto dall'utente
    attrazione = models.ForeignKey(to='Attrazione', on_delete=models.CASCADE, related_name="attrazione")
    # utente = models.ForeignKey(to=profiles.models.UserProfileModel, related_name='Utente', on_delete=models.CASCADE)
    oraInizio = models.TimeField(blank=True)  # scelta dall'utente
    oraFine = models.TimeField(blank=True)  # scelta dall'utente
    durata = models.DurationField()  # questi sono i secondi della durata
    posizioneInGiornata = models.IntegerField()  # numero progressivo

    def __str__(self):
        return "ID: " + str(self.pk) + "scelta: " + str(self.attrazione) + " , il " + str(self.giorno)

    class Meta:
        verbose_name = "Scelta"
        verbose_name_plural = "Scelte"
    # override del metodo save
    # controllare che ora inizio e fine siano ammissibili


class Giornata(models.Model):
    data = models.DateField()
    numeroGiornata = models.IntegerField()
    totAttrazioni = models.IntegerField()
    totCosto = models.FloatField()
    scelte = models.ManyToManyField(Scelta, related_name='giornate')

    def __str__(self):
        return "ID: " + str(self.pk) + "giorno: " + str(self.data) + " , num " + str(self.numeroGiornata)

    class Meta:
        verbose_name = "Giornata"
        verbose_name_plural = "Giornate"


class Vacanza(models.Model):
    dataArrivo = models.DateField()
    dataPartenza = models.DateField()
    nrPersone = models.IntegerField()
    budgetDisponibile = models.FloatField()
    totGiorni = models.IntegerField()
    totNotti = models.IntegerField()
    giornata = models.ManyToManyField(Giornata, related_name='vacanze')

    def __str__(self):
        return "ID: " + str(self.pk) + "inizio: " + str(self.dataArrivo) + " , fine: " + str(self.dataPartenza)

#  TODO provare a spostarlo nella view tramite la funzione post
    def calcolaGiorniNotti(self):
        totGiorni = abs(Vacanza.dataArrivo - Vacanza.dataPartenza) +1
        totGiorni = totGiorni.day
        totNotti = abs(Vacanza.dataArrivo - Vacanza.dataPartenza)
        totNotti = totNotti.day
    class Meta:
        verbose_name = "Vacanza"
        verbose_name_plural = "Vacanze"
