from django.db import models
from profiles.models import UserProfileModel
from attractions.models import Attrazione


class Scelta(models.Model):
    giorno = models.DateField()  # scelto dall'utente
    attrazione = models.ForeignKey(to='attractions.Attrazione', on_delete=models.CASCADE, related_name="attrazione")
    oraInizio = models.TimeField(blank=True)  # scelta dall'utente
    oraFine = models.TimeField(blank=True)  # scelta dall'utente
    durata = models.DurationField()  # questi sono i secondi della durata
    tempo_spostamento = models.DurationField(null=True)
    tipo_spostamento = models.CharField(null=True)
    def __str__(self):
        return "ID: " + str(self.pk) + "scelta: " + str(self.attrazione) + " , il " + str(self.giorno)

    class Meta:
        verbose_name = "Scelta"
        verbose_name_plural = "Scelte"

    # controllo ammissibilità ora inizio e fine, da chiamare nella creazione della scelta
    def orari_ammissibili(self):
        ammissibile = False
        if self.attrazione.oraApertura < (self.oraInizio and self.oraFine) < self.attrazione.oraChiusura:
            if self.oraInizio < self.oraFine:
                ammissibile = True
        return ammissibile


class Vacanza(models.Model):
    dataArrivo = models.DateField()
    dataPartenza = models.DateField()
    nrPersone = models.IntegerField()
    budgetDisponibile = models.FloatField()
    utente = models.ForeignKey(UserProfileModel, related_name='Utente', on_delete=models.PROTECT)
    scelte = models.ManyToManyField(Scelta, related_name='vacanze')

    def __str__(self):
        return "ID: " + str(self.pk) + " , inizio: " + str(self.dataArrivo) + " , fine: " + str(self.dataPartenza)

    def calcolaGiorni(self):
        totGiorni = abs(self.dataPartenza - self.dataArrivo)
        return totGiorni.days + 1

    def calcolaNotti(self):
        totNotti = abs(self.dataPartenza - self.dataPartenza)
        return totNotti.days

    def calcolaTotale(self):
        totale = 0
        for s in self.scelte:
            totale = totale + s.attrazione.costo
        return totale

    class Meta:
        verbose_name = "Vacanza"
        verbose_name_plural = "Vacanze"
