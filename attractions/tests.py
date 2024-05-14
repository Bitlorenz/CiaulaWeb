from datetime import time
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from profiles.models import UserProfileModel
from .models import Attrazione
from .views import CancellaAttrazione


# Test sulla cancellazione di un'attrazione
class DeleteAttrazioneViewTest(TestCase):

    def setUp(self):
        # Dati admin e attrazione di test
        self.user = UserProfileModel.objects.create_user(email='testadmin@mail.com', password='testadminpassword', is_admin=True)
        self.attrazione = Attrazione.objects.create(nome='Attrazione Test',
                                                    luogo='Luogo Test',
                                                    via='Via Test',
                                                    citta='Citta Test',
                                                    costo=1.10,
                                                    tipo='Tipo Test',
                                                    oraApertura=time(10,10,10),
                                                    oraChiusura=time(11,11,11),
                                                    descrizione="Descrizione Test")

    def test_cancella_attrazione(self):
        request_factory = RequestFactory()
        # Crea una richiesta con un admin autenticato
        request = request_factory.delete(reverse('attractions:cancella_attrazione', kwargs={'pk': self.attrazione.pk}))
        request.user = self.user
        # Creo la view
        view = CancellaAttrazione()
        view.setup(request, pk=self.attrazione.pk)
        # Chiamo test_func per controllare se l'utente admin ha i permessi
        self.assertTrue(view.test_func())
        # Check se la view ritorna il corretto success URL dopo la rimozione
        response = view.delete(request, pk=self.attrazione.pk)
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Attrazione.objects.filter(pk=self.attrazione.pk).exists()) #controllo cancellazione attrazione
        response.client = Client()
        self.assertRedirects(response, reverse('attractions:attrazioni'))

    def test_cancella_attrazione_no_permessi(self):
        request_factory = RequestFactory()
        # Crea una richiesta con un utente autenticato non-admin
        request = request_factory.delete(reverse('attractions:cancella_attrazione', kwargs={'pk': self.attrazione.pk}))
        self.user.is_admin = False
        request.user = self.user
        view = CancellaAttrazione()
        view.setup(request, pk=self.attrazione.pk)
        # Chiama test_func per controllare che l'user non admin abbia i permessi 
        self.assertFalse(view.test_func())
        # Chiama handle_no_permission e controlla se ritorna HttpResponseForbidden
        response = view.handle_no_permission()
        self.assertEqual(response.status_code, 403)

