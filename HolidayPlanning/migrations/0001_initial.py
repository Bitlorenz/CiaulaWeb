# Generated by Django 4.1.2 on 2022-11-06 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attrazione',
            fields=[
                ('nome', models.CharField(max_length=200, primary_key=True, serialize=False)),
                ('luogo', models.CharField(max_length=300)),
                ('via', models.CharField(max_length=500)),
                ('citta', models.CharField(max_length=200)),
                ('costo', models.FloatField()),
                ('tipo', models.CharField(max_length=200)),
                ('oraApertura', models.DateTimeField(verbose_name='ora apertura')),
                ('oraChiusura', models.DateTimeField(verbose_name='ora chiusura')),
                ('descrizione', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Giornata',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField()),
                ('numeroGiornata', models.IntegerField()),
                ('totAttrazioni', models.IntegerField()),
                ('totCosto', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Vacanza',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dataArrivo', models.DateTimeField()),
                ('dataPartenza', models.DateTimeField()),
                ('nrPersone', models.IntegerField()),
                ('budgetDisponibile', models.FloatField()),
                ('totGiorni', models.IntegerField()),
                ('totNotti', models.IntegerField()),
                ('giornata', models.ManyToManyField(related_name='vacanze', to='HolidayPlanning.giornata')),
            ],
        ),
        migrations.CreateModel(
            name='Scelta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('giorno', models.DateTimeField()),
                ('oraInizio', models.DateTimeField(blank=True)),
                ('oraFine', models.DateTimeField(blank=True)),
                ('durata', models.DurationField()),
                ('posizioneInGiornata', models.IntegerField()),
                ('attrazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attrazione', to='HolidayPlanning.attrazione')),
            ],
        ),
        migrations.AddField(
            model_name='giornata',
            name='scelte',
            field=models.ManyToManyField(related_name='giornate', to='HolidayPlanning.scelta'),
        ),
    ]
