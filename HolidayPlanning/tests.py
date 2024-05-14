from django.test import TestCase, RequestFactory
from django.urls import reverse
from attractions.models import Attrazione
from django.core.exceptions import ValidationError
from profiles.models import UserProfileModel
from .models import Vacanza, Scelta
from .views import scegliattrazione


class TestScegliAttrazioneView(TestCase):
    def setUp(self):
        email_unica = f"{self._testMethodName}@utente.it"
        self.turista = UserProfileModel.objects.create_user(email=email_unica, password="testscegliattrazione")
        # self.turista.save()
        self.vacanza = Vacanza.objects.create(nome='Test Vacanza', dataArrivo='2024-05-15', dataPartenza='2024-05-20',
                                               nrPersone=2, budgetDisponibile=1000.00, utente=self.turista)
        self.attrazione = Attrazione.objects.create(nome='Test Attrazione')
        self.url = reverse('scegli_attrazione', args=[self.attrazione.pk, self.vacanza.pk])

    def test_scegliattrazione_post(self):
        request = RequestFactory().post(self.url, {'giorno': '2024-05-16', 'oraInizio': '10:00', 'oraFine': '12:00'})
        request.user = self.turista
        response = scegliattrazione(request, self.attrazione.pk, self.vacanza.pk)
        self.assertEqual(response.status_code, 302)  # Controllo la redirezione dopo una corretta immissione del form

        scelta = Scelta.objects.last()
        self.assertEqual(scelta.giorno, '2024-05-16')
        self.assertEqual(scelta.oraInizio.strftime('%H:%M'), '10:00')
        self.assertEqual(scelta.oraFine.strftime('%H:%M'), '12:00')
        self.assertEqual(scelta.attrazione, self.attrazione)
        self.assertIn(scelta, self.vacanza.scelte.all())
        
    def test_checkOrariGiorno_validation_error(self):
        # Creo un oggetto Scelta con il giorno non compreso tra dataArrivo e dataPartenza
        giorno_fuori_vacanza = '2024-05-21'
        request = RequestFactory().post(self.url, {'giorno': giorno_fuori_vacanza, 'oraInizio': '10:00', 'oraFine': '12:00'})
        request.user = self.turista

        # Mi aspetto che venga sollevato un ValidationError da checkOrariGiorno
        with self.assertRaises(ValidationError):
            scegliattrazione(request, self.attrazione.pk, self.vacanza.pk)

    def test_scegliattrazione_get(self):
        request = RequestFactory().get(self.url)
        request.user = self.turista
        response = scegliattrazione(request, self.attrazione.pk, self.vacanza.pk)
        self.assertEqual(response.status_code, 200)  # Controlla se la view ritorna una risposta con status code 200


