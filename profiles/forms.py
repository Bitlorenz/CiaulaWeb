from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from profiles.models import UserProfileModel
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


# Un form per creare nuovi utenti. Include tutti i campi richiesti e una password ripetuta
class UserProfileForm(UserCreationForm):
    # password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Conferma Password', widget=forms.PasswordInput)
    helper = FormHelper()
    helper.form_id = 'user_profile_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('save', 'Save'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserProfileModel
        fields = ['first_name', 'last_name', 'email', 'codiceFiscale', 'telefono', 'dataDiNascita', 'profile_image']
        labels = {'first_name': _('Nome'), 'last_name': _('Cognome'),
                  'codiceFiscale': _('Codice Fiscale'), 'telefono': _('Telefono'),
                  'dataDiNascita': _('Data di Nascita'), 'profile_image': _('Immagine Profilo')}

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
        # Save the provided password in hashed format
        print("chiamata la funzione save di UserCreationForm ")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserUpdateForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'user_profile_crispy_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('save', 'Save'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = UserProfileModel
        fields = ['first_name', 'last_name', 'email', 'codiceFiscale', 'telefono', 'dataDiNascita', 'profile_image']
# A form for updating users. Includes all the fields on
# the user, but replaces the password field with admin's
# disabled password hash display field.
# class UserChangeForm(forms.ModelForm):
#    password = ReadOnlyPasswordHashField()

#    class Meta:
#        model = UserProfileModel
#        fields = ('email', 'password', 'is_active', 'is_admin')
