from django.db import models
from datetime import *
'''classe modello per l'attrazione'''
class Attrazione(models.Model):
    nome = models.CharField(max_length=200)
    posizione = models.CharField(max_length=300)
    costo = models.FloatField(default=10.5)
    durata = models.DurationField#questi sono i secondi della durata
    tipo = models.CharField(max_length=200)
    oraInizio = models.DateTimeField('ora inizio')
    oraFine = models.DateTimeField('ora fine')

    #override del metodo save
    def save(self, *args, **kwargs):
        self.durata = self.oraFine - self.oraInizio
        super(Attrazione, self).save(*args, **kwargs)#chiamata al vero metodo save
    #def __str__(self):
    #   return  self.__str__(self.nome, self.posizione, self.tipo)

class Giornata(models.Model):
    numero = models.IntegerField#TODO chiave
    attrazioni = models.ForeignKey(Attrazione, on_delete=models.CASCADE)
    #attrazioni = models.CharField(max_length=500)#TODO è una lista di attrazioni salvate sul db
    oraSveglia = models.DateTimeField('ora Sveglia')
    oraRientro = models.DateTimeField('Ora Rientro')

    def __str__(self):
        return self.Giornata_text


