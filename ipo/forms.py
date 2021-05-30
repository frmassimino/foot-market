from django import forms

from .models import Bidder, Ipo

class IpoModelForm(forms.ModelForm):
    class Meta:
        model = Bidder
        fields = [
            'value'
        ]
        widgets = {'bidder': forms.HiddenInput(),
        'status': forms.HiddenInput(),
        'ipo': forms.HiddenInput(),
        'value_last': forms.HiddenInput(),
        'value_actual': forms.HiddenInput()}

    #Validación en el form y no en el video
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value == int:
            raise forms.ValidationError("This is not a valid value")
        return value

