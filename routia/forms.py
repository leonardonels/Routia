from django import forms

class ChangeUsernameForm(forms.Form):
    new_username = forms.CharField(max_length=150, required=True, label='New Username')
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        new_username = cleaned_data.get('new_username')
        password = cleaned_data.get('password')

        if new_username and password:
            if not self.user.check_password(password):
                raise forms.ValidationError('Incorrect password.')

        return cleaned_data

class DeleteProfileForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not self.user.check_password(password):
            raise forms.ValidationError('Incorrect password.')
        return password