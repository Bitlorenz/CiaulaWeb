from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from profiles.models import UserProfileModel

"""A form for creating new users. Includes all the required
        fields, plus a repeated password."""


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Conferma Password', widget=forms.PasswordInput)

    class Meta:
        model = UserProfileModel
        fields = ['first_name', 'last_name', 'email', 'codiceFiscale', 'telefono', 'dataDiNascita']
        labels = {'first_name': _('Nome'), 'last_name': _('Cognome'),
                  'codiceFiscale': _('Codice Fiscale'), 'telefono': _('Telefono'),
                  'dataDiNascita': _('Data di Nascita')}

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        print("chiamata la funzione save di UserCreationForm ")
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


# A form for updating users. Includes all the fields on
# the user, but replaces the password field with admin's
# disabled password hash display field.
class UserChangeForm(forms.ModelForm):

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = UserProfileModel
        fields = ('email', 'password', 'is_active', 'is_admin')
