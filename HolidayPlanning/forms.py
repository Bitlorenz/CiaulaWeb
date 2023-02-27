from django import forms


class SearchForm(forms.Form):
    CHOICE_LIST = [("Attrazione", "Cerca nelle Attrazioni"),
                   ("Scelta", "Cerca nelle Scelte")]

    search_string = forms.CharField(label="Cosa cerchi?", max_length=100, min_length=1, required=True)
    search_where = forms.ChoiceField(label="Dove lo cerchi?", required=True, choices=CHOICE_LIST)
