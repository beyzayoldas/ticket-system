from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth.models import User
from tickets import admin
from .models import CustomUser, Ticket, TicketUpdate, Yer, ProgramModule
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model

class CustomUserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True


class AdminUserChangeForm(UserChangeForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user


LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('de', 'German'),
    ('el', 'Greek'),
    ('es', 'Spanish'),
    ('es_AR', 'Spanish (Argentina)'),
    ('es_MX', 'Spanish (Mexico)'),
    ('fr', 'French'),
    ('it', 'Italian'),
    ('ja', 'Japanese'),
    ('nl', 'Dutch'),
    ('pl', 'Polish'),
    ('pt_BR', 'Portuguese (Brazil)'),
    ('ru', 'Russian'),
    ('tr', 'Turkish'),
    ('zh_CN', 'Chinese (China)'),
    ('zh_TW', 'Chinese (Taiwan)'),
]

class UserProfileForm(UserChangeForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=False, label="Confirm Password")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'language', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')

        if password and password != password_confirm:
            self.add_error('password_confirm', 'Passwords do not match')

        return cleaned_data

    def save(self, commit=True):
        user = super(UserProfileForm, self).save(commit=False)
        password = self.cleaned_data['password']
        if password:
            user.password = make_password(password)
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):
    language = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'language']

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)

class TicketForm(forms.ModelForm):
    email_notification = forms.ModelMultipleChoiceField(
        queryset=CustomUser.objects.filter(is_active=True),  # Yalnızca aktif kullanıcıları filtrele
        widget=forms.CheckboxSelectMultiple(),
        required=False,
        label="E-Posta bildirisi gönder"
    )

    class Meta:
        model = Ticket
        fields = ['summary', 'details', 'company', 'priority', 'severity', 
                  'special_group', 'ticket_type', 'assigned_to', 'email_notification', 'attachment']

    def __init__(self, *args, **kwargs):
        super(TicketForm, self).__init__(*args, **kwargs)
        self.fields['summary'].widget.attrs.update({'class': 'form-control'})
        self.fields['details'].widget.attrs.update({'class': 'form-control'})
        self.fields['company'].widget.attrs.update({'class': 'form-control'})
        self.fields['priority'].widget.attrs.update({'class': 'form-control'})
        self.fields['severity'].widget.attrs.update({'class': 'form-control'})
        self.fields['special_group'].widget.attrs.update({'class': 'form-control'})
        self.fields['ticket_type'].widget.attrs.update({'class': 'form-control'})
        self.fields['assigned_to'].queryset = CustomUser.objects.filter(is_active=True)  # Yalnızca aktif kullanıcıları filtrele
        self.fields['email_notification'].widget.attrs.update({'class': 'form-check-input'})  # Checkbox için uygun sınıf
        self.fields['attachment'].widget.attrs.update({'class': 'form-control-file'})


class YerForm(forms.ModelForm):
    class Meta:
        model = Yer
        fields = ['goruntu_adi', 'kisa_ad', 'tanim', 'genel_yap']


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='İsminizi girin')
    last_name = forms.CharField(max_length=30, required=True, help_text='Soyadınızı girin')

    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'language', 'password1', 'password2')


class TicketUpdateForm(forms.ModelForm):
    class Meta:
        model = TicketUpdate
        fields = ['comment', 'status']


class KullaniciAtaForm(forms.Form):
    kullanici = forms.ModelChoiceField(queryset=CustomUser.objects.all(), label="Kullanıcı")
    rol = forms.ChoiceField(choices=[('ENDUSER', 'ENDUSER'), ('ITMANAGER', 'ITMANAGER'), ('OTHERMANAGER', 'OTHERMANAGER'), ('ITSTAFF', 'ITSTAFF')], label="Rol")
