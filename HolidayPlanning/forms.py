from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from models import Vacanza


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
    #TODO valutare opzione Save
    helper.add_input(Submit('submit', 'Submit'))
    helper.inputs[0].field_classes = 'btn btn-success'
    class Meta:
        model = Vacanza
        fields = ['dataArrivo', 'dataPartenza', 'nrPersone', 'budgetDisponibile']
