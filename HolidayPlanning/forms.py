from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import get_object_or_404
from .models import Vacanza, Scelta, Spostamento
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
        fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile', 'nome']


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
        self.fields['attrazione'].initial = a.citta
        self.fields['attrazione'].disabled = True
        self.fields['attrazione'].widget.attrs["readonly"] = True

    class Meta:
        model = Scelta
        fields = ['attrazione', 'giorno', 'oraInizio', 'oraFine']


class ModificaSceltaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'scelta-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Modifica'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Scelta
        fields = ['giorno', 'oraInizio', 'oraFine']


class SpostamentoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'scelta-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Aggiungi'))
    helper.inputs[0].field_classes = 'btn btn-success'

    def __init__(self, *args, **kwargs):
        super(SpostamentoForm, self).__init__(*args, **kwargs)
        self.fields['scelta_partenza'].widget.attrs['readonly'] = True
        self.fields['scelta_arrivo'].widget.attrs['readonly'] = True
        self.fields['scelta_partenza'].disabled = True
        self.fields['scelta_arrivo'].disabled = True

    class Meta:
        model = Spostamento
        fields = ['scelta_partenza', 'scelta_arrivo', 'ora_partenza', 'ora_arrivo', 'durata_spostamento', 'veicolo',
                  'tipo_spostamento', 'costo']
