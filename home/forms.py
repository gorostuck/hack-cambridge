from django import forms


class SearchForm(forms.Form):
    keyword = forms.CharField(label='I want to find the best', max_length=100)
    location = forms.CharField(label='in ', max_length=100)
