from django import forms

class SearchForm(forms.Form):
	keywords = forms.CharField(max_length=36, required=False)
