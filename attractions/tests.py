from datetime import time

from django.test import TestCase, RequestFactory
from django.urls import reverse
from profiles.models import UserProfileModel
from .models import Attrazione
from .views import CancellaAttrazione


# Test sulla cancellazione di un'attrazione
class DeleteAttrazioneViewTest(TestCase):

    def setUp(self):
        # Dati admin e attrazione di test
        self.user = UserProfileModel.objects.create_user(email='testuser@mail.com', password='testpassword')
        self.attrazione = Attrazione.objects.create(nome='Attrazione Test',
                                                    luogo='Luogo Test',
                                                    via='Via Test',
                                                    citta='Citta Test',
                                                    costo=1.10,
                                                    tipo='Tipo Test',
                                                    oraApertura=time(10,10,10),
                                                    oraChiusura=time(11,11,11),
                                                    descrizione="Descrizione Test")

    def test_cancella_attrazione_view(self):
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
        self.assertFalse(Attrazione.objects.filter(pk=self.attrazione.pk).exists()) #controllo cancellazione attrazione
        self.assertRedirects(response, reverse('attractions:attrazioni'))

    def test_cancella_falsa_attrazione_view(self):
        request_factory = RequestFactory()
        request = request_factory.delete(reverse('attractions:cancella_attrazione', kwargs={'pk': 'Sole, Mare, Vento'}))
        request.user = self.user
        view = CancellaAttrazione()
        view.setup(request, pk='Sole, Mare, Vento')
        response = view.delete(request, pk='Sole, Mare, Vento')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Attrazione.objects.filter(pk=self.attrazione.pk).exists())

    def test_cancella_attrazione_view_no_permission(self):
        # Create a request factory
        request_factory = RequestFactory()

        # Create a request with an authenticated non-admin user
        request = request_factory.delete(reverse('your_app:cancella_attrazione', kwargs={'pk': self.attrazione.pk}))
        request.user = self.user

        # Instantiate the view
        view = CancellaAttrazione()
        view.setup(request, pk=self.attrazione.pk)

        # Call test_func to check if the non-admin user has permission
        self.assertFalse(view.test_func())

        # Call handle_no_permission and check if it returns HttpResponseForbidden
        response = view.handle_no_permission()
        self.assertEqual(response.status_code, 403)

    def test_get_context_data(self):
        # Create a request factory
        request_factory = RequestFactory()

        # Create a request with an authenticated admin user
        request = request_factory.get(reverse('your_app:cancella_attrazione', kwargs={'pk': self.attrazione.pk}))
        request.user = self.admin_user

        # Instantiate the view
        view = CancellaAttrazione()
        view.setup(request, pk=self.attrazione.pk)

        # Call get_context_data and check if it returns the correct context
        context = view.get_context_data()
        self.assertEqual(context['title'], 'Cancella Attrazione')
        self.assertEqual(context['attr'], self.attrazione)


