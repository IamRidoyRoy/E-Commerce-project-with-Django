from django import forms
from .models import Account


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Enter password"
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': "Enter password again"
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name',
                  'phone_number', 'email', 'password']

    # Password validations
    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password doesn't match!"
            )

    # Form design
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

        # create placeholder
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter first name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter last name'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter email addresss'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter phone number'

        # Give css on the form
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
