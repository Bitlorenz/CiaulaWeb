from django.db import models
from profiles.models import UserProfileModel
from attractions.models import Attrazione


class Scelta(models.Model):
    giorno = models.DateField()  # scelto dall'utente
    attrazione = models.ForeignKey(to='attractions.Attrazione', on_delete=models.CASCADE, related_name="attrazione")
    oraInizio = models.TimeField(blank=True)  # scelta dall'utente
    oraFine = models.TimeField(blank=True)  # scelta dall'utente
    durata = models.DurationField()  # questi sono i secondi della durata

    def __str__(self):
        return "ID: " + str(self.pk) + "scelta: " + str(self.attrazione) + " , il " + str(self.giorno)

    class Meta:
        verbose_name = "Scelta"
        verbose_name_plural = "Scelte"

    def next_scelta(self):
        next_scelta = Scelta.objects.filter(giorno=self.giorno, oraInizio__gt=self.oraFine).order_by(
            'oraInizio').first()
        if next_scelta:
            return next_scelta
        else:
            return None

    # controllo ammissibilità ora inizio e fine, da chiamare nella creazione della scelta
    def orari_ammissibili(self):
        ammissibile = False
        if self.attrazione.oraApertura < (self.oraInizio and self.oraFine) < self.attrazione.oraChiusura:
            if self.oraInizio < self.oraFine:
                ammissibile = True
        return ammissibile


class Spostamento(models.Model):
    scelta_partenza = models.ForeignKey(Scelta, on_delete=models.SET_NULL, null=True, related_name="partenza")
    scelta_arrivo = models.ForeignKey(Scelta, on_delete=models.SET_NULL, null=True, related_name="arrivo")
    ora_partenza = models.TimeField(blank=True)
    ora_arrivo = models.TimeField(blank=True)
    durata_spostamento = models.DurationField(blank=True, null=True)  # può essere omesso, in tal caso viene calcolato
    veicolo = models.CharField(max_length=30, blank=True)
    tipo_spostamento = models.CharField(max_length=10)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True)  # dovrebbe influenzare il budget della vacanza

    def __str__(self):
        return "Spostamento da: "+str(self.scelta_partenza.attrazione.citta)+" a "+str(self.scelta_arrivo.attrazione.citta)

    class Meta:
        verbose_name = "Spostamento"
        verbose_name_plural = "Spostamenti"


class Vacanza(models.Model):
    nome = models.CharField(max_length=300, blank=True)
    dataArrivo = models.DateField()
    dataPartenza = models.DateField()
    nrPersone = models.IntegerField()
    budgetDisponibile = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    utente = models.ForeignKey(UserProfileModel, related_name='Utente', on_delete=models.PROTECT)
    scelte = models.ManyToManyField(Scelta, related_name='vacanze')
    spostamenti = models.ManyToManyField(Spostamento, related_name='spostamenti')

    def __str__(self):
        return "ID: " + str(self.pk) + " , inizio: " + str(self.dataArrivo) + " , fine: " + str(self.dataPartenza)

    def calcolaGiorni(self):
        totGiorni = abs(self.dataPartenza - self.dataArrivo)
        return totGiorni.days + 1

    def calcolaNotti(self):
        totNotti = abs(self.dataPartenza - self.dataPartenza)
        return totNotti.days

    def calcolaTotaleAttrazioni(self):
        totaleScelte = 0
        totaleSpostamenti = 0
        for s in self.scelte.all():
            totaleScelte = totaleScelte + s.attrazione.costo
        for s in self.spostamenti.all():
            totaleSpostamenti = totaleSpostamenti + s.costo
        return totaleScelte+totaleSpostamenti

    # metodo per calcolare il livello di difficoltà di una giornata basato sul numero di scelte in una giornata
    def difficolta_giornata(self):
        # Raggruppo le scelte per giornata
        scelte_per_giorno = {}
        for scelta in self.scelte.all():
            giorno_scelta = scelta.giorno.day
            if giorno_scelta not in scelte_per_giorno:
                scelte_per_giorno[giorno_scelta] = []
            scelte_per_giorno[giorno_scelta].append(scelta)

        # Determino livelli di difficoltà per ogni giorno
        difficulty_levels = {}
        for giorno_scelta, scelte_nel_giorno in scelte_per_giorno.items():
            count = len(scelte_nel_giorno)
            if count > 4:
                difficulty_levels[giorno_scelta] = "Difficile"
            elif count == 2 or count == 3:
                difficulty_levels[giorno_scelta] = "Media"
            else:
                difficulty_levels[giorno_scelta] = "Facile"

        return difficulty_levels

    def sort_scelte(self):
        return self.scelte.all().order_by('giorno', 'oraInizio', 'oraFine')

    class Meta:
        verbose_name = "Vacanza"
        verbose_name_plural = "Vacanze"
