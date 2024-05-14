from django.test import Client, TestCase
from django.urls import reverse_lazy
from profiles.models import UserProfileModel

class ProfileTest(TestCase):
    # setup dove creo un nuovo utente nel db
    def setUp(self):
        self.created_user = UserProfileModel.objects.create_user(email='prova@prova.it',
                                                                 password='Tentativo.1')

    def test_registration(self):
        client = Client()
        response = client.post(reverse_lazy('profiles:registration'), {
                            'email': 'prova@prova.it',
                            'password1': 'Tentativo.1',
                            'password2': 'Tentativo.1'
                            }, follow=True)

        self.assertEqual(response.status_code, 200)
        response = client.login(email='prova@prova.it', password='Tentativo.1')
        self.assertTrue(response)
        # controllo se riesco a loggare un utente creato
        def test_login_successful(self):
            client = Client()
            response = client.login(email='prova@prova.it', password='Tentativo.1')
            self.assertTrue(response)

        #controllo se riesco a non loggare un utente fasullo
        def test_login_unsuccessful(self):
            client = Client()
            response = client.login(email='non@esiste.it', password='F4ls4-password')

