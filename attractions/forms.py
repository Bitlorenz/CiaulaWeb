from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from attractions.models import Attrazione, Recensione
import gettext
_ = gettext.gettext


class SearchForm(forms.Form):
    CHOICE_LIST = [("Attrazione", "Cerca nelle Attrazioni"),
                   ("Scelta", "Cerca nelle Scelte")]

    search_string = forms.CharField(label="Cosa cerchi?", max_length=100, min_length=1, required=True)
    search_where = forms.ChoiceField(label="Dove lo cerchi?", required=True, choices=CHOICE_LIST)


class CreaAttrazioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'attrazione-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit', 'Salva'))
    helper.inputs[0].field_classes = 'btn btn-success'

    def clean(self):
        if self.cleaned_data["oraApertura"] > self.cleaned_data["oraChiusura"]:
            raise forms.ValidationError(_("Valori non validi: Ora di Chiusura precede ora di Apertura"))

    class Meta:
        model = Attrazione
        fields = "__all__"


class CreaRecensioneForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = 'crea_recensione_form'
    helper.form_method = 'POST'
    helper.add_input(Submit('save', 'Salva'))
    helper.inputs[0].field_classes = 'btn btn-success'

    class Meta:
        model = Recensione
        fields = [
            'titolo',
            'contenuto',
            'valutazione'
        ]

