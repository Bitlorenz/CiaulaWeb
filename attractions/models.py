from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from profiles.models import UserProfileModel


class Attrazione(models.Model):
    objects = None
    nome = models.CharField(max_length=200, primary_key=True)
    luogo = models.CharField(max_length=300)
    via = models.CharField(max_length=500)
    citta = models.CharField(max_length=200)
    costo = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    tipo = models.CharField(max_length=200)
    oraApertura = models.TimeField('ora apertura')
    oraChiusura = models.TimeField('ora chiusura')
    descrizione = models.TextField()
    attrazione_image = models.ImageField(blank=True, null=True)  # , upload_to='attractionImages/')

    def __str__(self):
        return "ID: " + str(self.pk) + ": " + self.nome + " di tipo " + self.tipo + " a " + self.citta

    class Meta:
        verbose_name = "Attrazione"
        verbose_name_plural = "Attrazioni"

    @property
    def image_url(self):
        if self.attrazione_image and hasattr(self.attrazione_image, 'url'):
            return self.attrazione_image.url
        else:
            return "Immagine non disponibile"


class Recensione(models.Model):
    titolo = models.CharField(max_length=200, verbose_name='Titolo della recensione')
    contenuto = models.TextField(max_length=1000, verbose_name='Contenuto della recesione')
    valutazione = models.IntegerField(validators=[MaxValueValidator(5), MinValueValidator(0)],
                                      verbose_name='valutazione della recensione')
    autore = models.ForeignKey(UserProfileModel, related_name='autore_recensione',
                               on_delete=models.CASCADE)
    # one-to-many (un prodotto ha tante recensioni ma una recensione appartiene a un singolo prodotto)
    attrazione = models.ForeignKey(Attrazione, on_delete=models.CASCADE)
    data_creazione = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Recensione'
        verbose_name_plural = 'Recensioni'
