from django import forms

class UploadStock(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()

class VerStock(forms.Form):
    consulta = forms.CharField()


