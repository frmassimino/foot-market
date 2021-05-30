from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class UserModelForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'age'
        ]
        widgets = {'funds': forms.HiddenInput(),
        'status': forms.HiddenInput()}

    #Validación en el form y no en el video
    def clean_value(self):
        value = self.cleaned_data.get('value')
        if value == int:
            raise forms.ValidationError("This is not a valid value")
        return value

class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    age = forms.IntegerField(required=True)
    funds = forms.IntegerField(required=False,widget=forms.HiddenInput())

    class Meta:
        model = CustomUser
        #fields = ("username","first_name","last_name", "email", "age", "password1", "password2","funds")
        fields = ("username","first_name","last_name", "email", "age","funds")
        #widgets = {'funds': forms.HiddenInput()}

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        user.email = self.cleaned_data["email"]
        user.age = self.cleaned_data["age"]
        user.funds = self.cleaned_data["funds"]
        if commit:
            user.save()
        return user

class UserChangeForm(UserChangeForm):
    age = forms.IntegerField(required=False)
    funds = forms.IntegerField(required=False)

    class Meta:
        model = CustomUser
        #fields = ("username","first_name","last_name", "email", "age", "password1", "password2","funds")
        fields = ("username","first_name","last_name", "email", "age","funds")