from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.db.models import Max
from .models import Dealers
from PIL import Image

class RegistrationDealerForm(UserCreationForm):
    firstname = forms.CharField(required=True, label="First Name:")
    lastname = forms.CharField(required=True, label="Surname:")
    username = forms.CharField(required=True)
    telephone = forms.CharField(required=False, label="Telephone Number:")
    email = forms.EmailField(required=True, label="E-mail:")

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "telephone", "email", "password1", "password2")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('This e-mail address already exists, use a different e-mail address.')
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(RegistrationDealerForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Repeat password:"
        self.fields[
            'password1'].help_text = "Password should at least consist of 5 characters. Do not only use numbers."
        self.fields['password2'].help_text = "Repeat the password."
        self.error_messages = {
            'password_mismatch': ("Oops! The two given passwords do not match. Please try again."),
        }
        self.fields['username'].widget.attrs['placeholder'] = 'johndoe123'
        self.fields['firstname'].widget.attrs['placeholder'] = 'John'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Doe'
        self.fields['telephone'].widget.attrs['placeholder'] = '31612345678'
        self.fields['email'].widget.attrs['placeholder'] = 'john@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

    def save(self, commit=True):
        user = super(RegistrationDealerForm, self).save(commit=False)
        maxID = Dealers.objects.all().aggregate(Max('dealerID'))
        if maxID.get('dealerID__max') == None:
            user.id = 1
        else:
            user.id = maxID.get('dealerID__max') + 1

        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.telephone = self.cleaned_data['telephone']

        dealerEntry = Dealers(dealerID=user.id, username=user.username, email=user.email, name=user.first_name,
                              surname=user.last_name, telephone=user.telephone)
        dealerEntry.save()

        if commit:
            user.save()

        return user


class RegistrationAdminForm(UserCreationForm):
    firstname = forms.CharField(required=True, label="First Name:")
    lastname = forms.CharField(required=True, label="Surname:")
    username = forms.CharField(required=True)
    telephone = forms.CharField(required=False, label="Telephone Number:")
    email = forms.EmailField(required=True, label="E-mail:")
    superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "telephone", "email", "password1", "password2")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError('This e-mail address already exists, use a different e-mail address.')
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(RegistrationAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = "Password:"
        self.fields['password2'].label = "Repeat password:"
        self.fields[
            'password1'].help_text = "Password should at least consist of 5 characters. Do not only use numbers."
        self.fields['password2'].help_text = "Repeat the password."
        self.error_messages = {
            'password_mismatch': ("Oops! The two given passwords do not match. Please try again."),
        }
        self.fields['username'].widget.attrs['placeholder'] = 'johndoe123'
        self.fields['firstname'].widget.attrs['placeholder'] = 'John'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Doe'
        self.fields['telephone'].widget.attrs['placeholder'] = '31612345678'
        self.fields['email'].widget.attrs['placeholder'] = 'john@example.com'
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'
        self.fields['superuser'].widget.attrs.update({'class': 'registeradmincheckbox'})

    def save(self, commit=True):
        user = super(RegistrationAdminForm, self).save(commit=False)
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.telephone = self.cleaned_data['telephone']
        user.is_superuser = self.cleaned_data['superuser']
        user.is_staff = True

        if commit:
            user.save()

        return user



class OrderForm(forms.ModelForm):
    CHOICES_model = (('Shelby Super Snake', 'Shelby Super Snake'), ('Shelby F150', 'Shelby F150'),)
    CHOICES_colour = (('Blue', 'Blue'), ('Yellow', 'Yellow'),)
    model = forms.ChoiceField(choices=CHOICES_model, required=True)
    colour = forms.ChoiceField(choices=CHOICES_colour, required=True)

    # model = forms.CharField(required=True)
    # colour = forms.CharField(required=True)

    class Meta:
        model = models.Orders
        fields = ("model", "colour")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['model'].label = "Model"
        self.fields['colour'].label = "Colour"
        self.fields['model'].widget.attrs['placeholder'] = 'Modelnumber'
        self.fields['colour'].widget.attrs['placeholder'] = 'What colour?'


class VehicleForm(forms.ModelForm):
    model = forms.CharField(required=True)
    headline = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    image = forms.ImageField()
    field_order = ['model', 'headline', 'description', 'image']

    class Meta:
        model = models.Vehicles
        fields = ("model", "headline", "description", "image")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = ""
        self.fields['model'].label = "Model"
        self.fields['headline'].label = "Headline"
        self.fields['description'].label = "Description"

        self.fields['image'].widget.attrs.update({'class': 'invis'})
        self.fields['model'].widget.attrs['placeholder'] = 'Shelby Supersnake'
        self.fields['headline'].widget.attrs['placeholder'] = 'Shelby Supersnake is one of the most..'
        self.fields['description'].widget.attrs['placeholder'] = 'A description of the model'

