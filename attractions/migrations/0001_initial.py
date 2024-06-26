# Generated by Django 4.2 on 2024-02-23 16:00

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
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
                ('oraApertura', models.TimeField(verbose_name='ora apertura')),
                ('oraChiusura', models.TimeField(verbose_name='ora chiusura')),
                ('descrizione', models.TextField()),
                ('attrazione_image', models.ImageField(blank=True, null=True, upload_to='')),
            ],
            options={
                'verbose_name': 'Attrazione',
                'verbose_name_plural': 'Attrazioni',
            },
        ),
        migrations.CreateModel(
            name='Recensione',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titolo', models.CharField(max_length=200, verbose_name='Titolo della recensione')),
                ('contenuto', models.TextField(max_length=1000, verbose_name='Contenuto della recesione')),
                ('valutazione', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(0)], verbose_name='valutazione della recensione')),
                ('data_creazione', models.DateTimeField(auto_now=True)),
                ('attrazione', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='attractions.attrazione')),
                ('autore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='autore_recensione', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Recensione',
                'verbose_name_plural': 'Recensioni',
            },
        ),
    ]
