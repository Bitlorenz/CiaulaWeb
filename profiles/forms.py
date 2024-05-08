from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Field
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from profiles.models import UserProfileModel


# Un form per creare nuovi utenti. Include tutti i campi richiesti e una password ripetuta
class UserCreationForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'create-user-form'
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'Aggiungi'))
    helper.inputs[0].field_classes = 'btn btn-success'
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Conferma Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfileModel
        fields = ['first_name', 'last_name', 'email', 'codiceFiscale', 'telefono', 'dataDiNascita', 'profile_image','password1','password2']
        labels = {'first_name': _('Nome'), 'last_name': _('Cognome'),
                  'codiceFiscale': _('Codice Fiscale'), 'telefono': _('Telefono'),
                  'dataDiNascita': _('Data di Nascita'), 'profile_image': _('Immagine Profilo'),
                  'password1': _('Password'), 'password2': _('Conferma Password')}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    # Imposta immagine del profilo di default nel caso non venga inserita
    def clean_profile_image(self):
        profile_image = self.cleaned_data['profile_image']
        if not profile_image:
            profile_image = 'defaultuser.png'  # Imposta l'immagine di default
        return profile_image

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# Form per aggiornare gli utenti
class UserChangeForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'user-update-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('save', 'Save'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserProfileModel
        fields = ('first_name', 'last_name', 'codiceFiscale', 'telefono', 'dataDiNascita', 'profile_image', 'email')
