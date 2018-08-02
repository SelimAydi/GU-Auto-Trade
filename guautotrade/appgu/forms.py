from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from . import models
from django.db.models import Max
from .models import Dealers
from django_countries.fields import CountryField
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
        user.is_superuser = self.cleaned_data['superuser']
        user.is_staff = True

        dealerEntry = Dealers(dealerID=user.id, username=user.username, email=user.email, name=user.first_name,
                              surname=user.last_name, telephone=user.telephone)
        dealerEntry.save()

        if commit:
            user.save()

        return user



class OrderForm(forms.ModelForm):
    CHOICES_model = (('Shelby F150 Super Snake', 'Shelby F150 Super Snake'), ('Shelby F150 Offroad', 'Shelby F150 Offroad'), ('Shelby F150 Offroad Longbed', 'Shelby F150 Offroad Longbed'),)
    CHOICES_colour = (('Lightning Blue', 'Lightning Blue'), ('Ruby Red', 'Ruby Red'), ('Shadow Black', 'Shadow Black'), ('Oxford White', 'Oxford White'), ('Magnetic', 'Magnetic'),)
    model = forms.ChoiceField(choices=CHOICES_model, required=True)
    colour = forms.ChoiceField(choices=CHOICES_colour, required=True)
    additional_comments = forms.CharField(required=False, widget=forms.Textarea)
    homologation = forms.BooleanField(required=False)
    custom_clearance = forms.BooleanField(required=False)

    class Meta:
        model = models.Orders
        fields = ("model", "colour", "additional_comments")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['model'].label = "Model"
        self.fields['colour'].label = "Colour"
        self.fields['additional_comments'].label = "Additional Comments"
        self.fields['model'].widget.attrs['placeholder'] = 'Modelnumber'
        self.fields['colour'].widget.attrs['placeholder'] = 'What colour?'
        self.fields['additional_comments'].widget.attrs['placeholder'] = 'Put extra information or remarks here'
        self.fields['homologation'].label = "Homologation: "
        self.fields['custom_clearance'].label = "Custom Clearance: "
        self.fields['homologation'].widget.attrs.update({'class': 'registeradmincheckbox'})
        self.fields['custom_clearance'].widget.attrs.update({'class': 'registeradmincheckbox'})

    def save(self, commit=True):
        order = super(OrderForm, self).save(commit=False)
        order.model = self.cleaned_data['model']
        order.colour = self.cleaned_data['colour']
        order.additional_comments = self.cleaned_data['additional_comments']
        order.homologation = self.cleaned_data['homologation']
        order.custom_clearance = self.cleaned_data['custom_clearance']

        if commit:
            order.save()

        return order


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
        self.fields['model'].widget.attrs['placeholder'] = 'Shelby Super Snake'
        self.fields['headline'].widget.attrs['placeholder'] = 'Shelby Super Snake is one of the most..'
        self.fields['description'].widget.attrs['placeholder'] = 'A description of the model'

class NewsPostForm(forms.ModelForm):
    writtenby = forms.CharField(required=True)
    banner = forms.ImageField()
    title = forms.CharField(required=True)
    headline = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    quote = forms.CharField(required=True)
    quotefooter = forms.CharField(required=True)
    field_order = ['title', 'headline', 'writtenby', 'quote', 'quotefooter', 'description', 'banner']

    class Meta:
        model = models.Vehicles
        fields = ("title", "headline", 'writtenby', 'quote', 'quotefooter', "description", "banner")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(NewsPostForm, self).__init__(*args, **kwargs)
        self.fields['banner'].label = ""
        self.fields['title'].label = "Title"
        self.fields['headline'].label = "Headline"
        self.fields['writtenby'].label = "Author"
        self.fields['description'].label = "Description"
        self.fields['quote'].label = "Quote"
        self.fields['quotefooter'].label = "Quote Reference"

        self.fields['banner'].widget.attrs.update({'class': 'invis'})
        self.fields['title'].widget.attrs['placeholder'] = 'Shelby Super Snake is amazing'
        self.fields['writtenby'].widget.attrs['placeholder'] = 'John Doe'
        self.fields['headline'].widget.attrs['placeholder'] = 'Shelby Super Snake is one of the most..'
        self.fields['quote'].widget.attrs['placeholder'] = 'Lorem ipsum dolor sit amet, consectetur adipiscing elit.'
        self.fields['quotefooter'].widget.attrs['placeholder'] = 'From Example.com'
        self.fields['description'].widget.attrs['placeholder'] = 'The actual newspost text goes here'

class EventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    link = forms.CharField(required=False)
    date = forms.CharField(required=True)
    field_order = ['title', 'link', 'date', 'description']

    class Meta:
        model = models.Vehicles
        fields = ("title", "description", "link")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Title"
        self.fields['description'].label = "Description"
        self.fields['date'].label = "Date"
        self.fields['link'].label = "Link"

        self.fields['title'].widget.attrs['placeholder'] = 'Shelby Drag Race'
        self.fields['description'].widget.attrs['placeholder'] = 'Information about the event'
        self.fields['link'].widget.attrs['placeholder'] = 'http://www.example.com/event'
        self.fields['date'].widget.attrs['placeholder'] = 'YYYY/MM/DD'
        self.fields['link'].help_text = "Optional. Leave blank if there is no link to the event."

class MapDealerForm(forms.ModelForm):
    customer_name = forms.CharField(required=True)
    email = forms.CharField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=True, widget=forms.Textarea)
    country = CountryField().formfield()
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)


    class Meta:
        model = models.Vehicles
        fields = ("customer_name", "email", "phone", "address", "country", "latitude", "longitude")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MapDealerForm, self).__init__(*args, **kwargs)
        self.fields['customer_name'].label = "Customer Name"
        self.fields['phone'].label = "Phone Number"
        self.fields['email'].label = "Email"
        self.fields['address'].label = "Address"
        self.fields['country'].label = "Country"

        self.fields['customer_name'].widget.attrs['placeholder'] = 'American Car City'
        self.fields['phone'].widget.attrs['placeholder'] = '33169221900'
        self.fields['email'].widget.attrs['placeholder'] = 'info@americancarcity.fr'
        self.fields['address'].widget.attrs['placeholder'] = '197 BD John Kennedy 91100 Corbeil-Essonnes'
        self.fields['latitude'].widget.attrs['placeholder'] = '48.579013'
        self.fields['longitude'].widget.attrs['placeholder'] = '2.4766'
        self.fields['phone'].help_text = "Optional field."
        self.fields['email'].help_text = "Optional field."



class PartialOrderForm(forms.ModelForm):

    invoice = forms.FileField(required=False)

    class Meta:
        model = models.Orders
        fields = ('invoice',)

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(PartialOrderForm, self).__init__(*args, **kwargs)
        self.fields['invoice'].label = ""
        self.fields['invoice'].required = False
        self.fields['invoice'].widget.attrs.update({'class': 'invis'})


class AdminOrderForm(OrderForm):
    forwho = forms.CharField(required=False)

    class Meta:
        model = models.Orders
        fields = ('forwho',) + OrderForm.Meta.fields

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['forwho'].label = "For User ID"
        self.fields['forwho'].help_text = "Leave blank if this order is on your name."
