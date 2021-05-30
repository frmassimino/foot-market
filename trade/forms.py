from django import forms

from .models import Bid,Ask

class BidModelForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = [
            'value'
        ]
        widgets = {'owner': forms.HiddenInput(), 
        'status': forms.HiddenInput(),
        #'trade':forms.HiddenInput(),
        'player': forms.HiddenInput(),
        'value_actual': forms.HiddenInput(),
        'value_last': forms.HiddenInput(),
        'date_created': forms.HiddenInput(),
        'date_updated': forms.HiddenInput()}

    #Validación en el form y no en el video
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value == int:
            raise forms.ValidationError("This is not a valid value")
        return value

class AskModelForm(forms.ModelForm):
    class Meta:
        model = Ask
        fields = [
            'value'
        ]
        widgets = {'owner': forms.HiddenInput(), 
        'status': forms.HiddenInput(),
        #'trade':forms.HiddenInput()
        'player': forms.HiddenInput(),
        'date_created': forms.HiddenInput(),
        'date_updated': forms.HiddenInput()}
    #Validación en el form y no en el video
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value == int:
            raise forms.ValidationError("This is not a valid value")
        return value