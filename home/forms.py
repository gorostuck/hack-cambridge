from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='I want to find the best', max_length=100)
    location = forms.CharField(label='in ', max_length=100)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""  # Removes : as label suffix
