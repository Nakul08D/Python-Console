from django import forms

class CodeInputForm(forms.Form):
    code = forms.CharField(widget=forms.Textarea, label='AWS Python Code')
