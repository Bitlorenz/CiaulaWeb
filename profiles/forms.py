from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm


class UserProfileForm(UserCreationForm):
    #override del metodo save per assicurarci di assegnare il gruppo specificato all'utente appena registrato.
    #I gruppi sono stati creati dal pannello web dell'admin.
    def save(self, commit=True):
        user = super().save(commit)  # ottengo un riferimento al turista
        g = Group.objects.get(name="Turisti")  # cerco il gruppo che mi interessa
        g.user_set.add(user)  # aggiungo l'utente al gruppo
        return user  # restituisco quello che il metodo padre di questo metodo avrebbe restituito


class ManagerProfileForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Manager")
        g.user_set.add(user)
        return user


