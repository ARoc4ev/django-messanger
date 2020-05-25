from django import forms
from .models import Account
from django.contrib.auth.forms import UserCreationForm




class RegisterForm(forms.ModelForm):

    class Meta:
        model = Account
        fields = ('email','password', 'last_name', 'first_name')


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user






class SettingForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name')