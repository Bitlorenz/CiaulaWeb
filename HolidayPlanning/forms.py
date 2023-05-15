from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import get_object_or_404

from .models import Vacanza, Scelta, Attrazione


class SearchForm(forms.Form):
    CHOICE_LIST = [("Attrazione", "Cerca nelle Attrazioni"),
                   ("Scelta", "Cerca nelle Scelte")]

    search_string = forms.CharField(label="Cosa cerchi?", max_length=100, min_length=1, required=True)
    search_where = forms.ChoiceField(label="Dove lo cerchi?", required=True, choices=CHOICE_LIST)


#  form per creare una vacanza
class CreaVacanzaForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'vacanza-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Crea Vacanza'))
    helper.inputs[0].field_classes = 'btn btn-success'
    class Meta:
        model = Vacanza
        fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile']


class ScegliAttrazioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'scelta-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Aggiungi'))
    helper.inputs[0].field_classes = 'btn btn-success'

    #def __init__(self, *args, **kwargs):
    #    self.attrazione_id = kwargs.pop('attrazione')
    #    super(ScegliAttrazioneForm, self).__init__(*args, **kwargs)

    def clean(self):
    #TODO bisogna mettere nella pagina l'id dell'attrazione da scegliere, si può mettere un choice field che recupera l'attrazione
    # da rivedere quando la primary key sarà passata tramite link
        #att = get_object_or_404(Attrazione, pk=self.cleaned_data["attrazione"].pk)
        oraInizioInput = self.cleaned_data["oraInizio"]
        oraFineInput = self.cleaned_data["oraFine"]
       # if not att.oraApertura < (self.oraInizio and self.oraFine) < att.oraChiusura:
       #     self.add_error("oraInizio", "Errore: orario non ammissibile")
       #     self.add_error("oraFine", "Errore: orario non ammissibile")
        if oraFineInput < oraInizioInput:
            self.add_error("oraInizio", "Errore: orario non ammissibile")
        return self.cleaned_data

    class Meta:
        model = Scelta
        fields = ['giorno', 'oraInizio', 'oraFine']

