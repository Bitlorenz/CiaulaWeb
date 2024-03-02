from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import get_object_or_404
from .models import Vacanza, Scelta
from attractions.models import Attrazione
import gettext
_ = gettext.gettext


#  form per creare una vacanza
class CreaVacanzaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'vacanza-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Crea Vacanza'))
    helper.inputs[0].field_classes = 'btn btn-success'

    def clean(self):
        if self.cleaned_data["dataArrivo"] > self.cleaned_data["dataPartenza"]:
            raise forms.ValidationError(_("Valori non validi: Data di Arrivo precede data di Partenza"))

    class Meta:
        model = Vacanza
        fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile']


# form per modificare una vacanza
class ModificaVacanzaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'vacanza-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Modifica'))
    helper.inputs[0].field_classes = 'btn btn-success'

    def clean(self):
        if self.cleaned_data["dataArrivo"] > self.cleaned_data["dataPartenza"]:
            raise forms.ValidationError(_("Valori non validi: Data di Arrivo precede data di Partenza"))

    class Meta:
        model = Vacanza
        fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile']


class ScegliAttrazioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'scelta-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Aggiungi'))
    helper.inputs[0].field_classes = 'btn btn-success'

    def __init__(self, pk, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = user
        a = get_object_or_404(Attrazione, pk=pk)
        self.attrazione = a
        self.fields['attrazione'].initial = a
        self.fields['attrazione'].disabled = True
        self.fields['attrazione'].widget.attrs["readonly"] = True

    def clean(self):
        a = self.attrazione
        ini = self.cleaned_data["oraInizio"]
        fine = self.cleaned_data["oraFine"]
        if fine < ini:
            raise forms.ValidationError(_("Valori non validi: Ora di Inizio precede Ora di Fine"))
        if not a.oraApertura <= ini <= a.oraChiusura:
            self.add_error("oraInizio",
                           "Inserire orario compreso tra: " + str(a.oraApertura) + " e " + str(a.oraChiusura))

            raise forms.ValidationError(_("Orario di Inizio non valido"))
        if not a.oraApertura <= fine <= a.oraChiusura:
            self.add_error("oraFine",
                           "Inserire orario compreso tra: " + str(a.oraApertura) + " e " + str(a.oraChiusura))
            raise forms.ValidationError(_("Orario di Fine non valido"))
        return self.cleaned_data

    class Meta:
        model = Scelta
        fields = ['attrazione', 'giorno', 'oraInizio', 'oraFine']


class SpostamentoForm(forms.ModelForm):
    pass
