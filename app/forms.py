from django import forms

class ReminderForm(forms.Form):
    date = forms.DateField(input_formats=['%d-%m-%Y'])
    time = forms.TimeField(input_formats=['%H:%M:%S'])
    message = forms.CharField(widget=forms.Textarea(attrs={'maxlength': 255}))