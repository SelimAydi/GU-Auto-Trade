from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy

from . import models
from django.db.models import Max
from .models import Dealers, MapDealers, Orders
from django_countries.fields import CountryField
from PIL import Image

class RegistrationDealerForm(UserCreationForm):
    firstname = forms.CharField(required=True, label=ugettext_lazy('First Name:'))
    lastname = forms.CharField(required=True, label=ugettext_lazy('Surname:'))
    username = forms.CharField(required=True, label=ugettext_lazy('Username:'))
    telephone = forms.CharField(required=False, label=ugettext_lazy('Telephone Number:'))
    email = forms.EmailField(required=True, label="E-mail:")

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "telephone", "email", "password1", "password2")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(ugettext_lazy('This e-mail address already exists, use a different e-mail address.'))
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(RegistrationDealerForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = ugettext_lazy('Password:')
        self.fields['password2'].label = ugettext_lazy('Repeat Password:')
        self.fields[
            'password1'].help_text = ugettext_lazy('Password should at least consist of 5 characters. Do not only use numbers.')
        self.fields['password2'].help_text = ugettext_lazy('Repeat the password:')
        self.error_messages = {
            'password_mismatch': ugettext_lazy("Oops! The two given passwords do not match. Please try again."),
        }
        self.fields['username'].widget.attrs['placeholder'] = 'johndoe123'
        self.fields['firstname'].widget.attrs['placeholder'] = 'John'
        self.fields['lastname'].widget.attrs['placeholder'] = 'Doe'
        self.fields['telephone'].widget.attrs['placeholder'] = '31612345678'
        self.fields['email'].widget.attrs['placeholder'] = ugettext_lazy('john@example.com')
        self.fields['password1'].widget.attrs['placeholder'] = '********'
        self.fields['password2'].widget.attrs['placeholder'] = '********'

    def save(self, commit=True):
        maxUserID = User.objects.all().aggregate(Max('id'))
        user = super(RegistrationDealerForm, self).save(commit=False)

        if maxUserID.get('id__max') == None:
            user.id = 1
        else:
            user.id = maxUserID.get('id__max') + 1

        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.telephone = self.cleaned_data['telephone']

        dealerEntry = Dealers(user=user, telephone=user.telephone)
        dealerEntry.save()

        if commit:
            user.save()

        return user


class RegistrationAdminForm(UserCreationForm):
    firstname = forms.CharField(required=True, label=ugettext_lazy("First Name:"))
    lastname = forms.CharField(required=True, label=ugettext_lazy("Surname:"))
    username = forms.CharField(required=True, label=ugettext_lazy("Username:"))
    telephone = forms.CharField(required=False, label=ugettext_lazy("Telephone Number:"))
    email = forms.EmailField(required=True, label=ugettext_lazy("E-mail:"))
    superuser = forms.BooleanField(required=False)

    class Meta:
        model = User
        fields = ("username", "firstname", "lastname", "telephone", "email", "password1", "password2")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data['email']).exists():
            raise forms.ValidationError(ugettext_lazy('This e-mail address already exists, use a different e-mail address.'))
        return self.cleaned_data['email']

    def __init__(self, *args, **kwargs):
        super(RegistrationAdminForm, self).__init__(*args, **kwargs)
        self.fields['password1'].label = ugettext_lazy("Password:")
        self.fields['password2'].label = ugettext_lazy("Repeat password:")
        self.fields[
            'password1'].help_text = ugettext_lazy("Password should at least consist of 5 characters. Do not only use numbers.")
        self.fields['password2'].help_text = ugettext_lazy("Repeat the password.")
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
        maxID = User.objects.all().aggregate(Max('id'))
        if maxID.get('id__max') == None:
            user.id = 1
        else:
            user.id = maxID.get('id__max') + 1

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
    CHOICES_model = (('Shelby F150 Super Snake', 'Shelby F150 Super Snake'), ('Shelby F150 Offroad', 'Shelby F150 Offroad'), ('Shelby F150 Offroad Longbed', 'Shelby F150 Offroad Longbed'),)
    CHOICES_colour = (('Lightning Blue', 'Lightning Blue'), ('Ruby Red', 'Ruby Red'), ('Shadow Black', 'Shadow Black'), ('Oxford White', 'Oxford White'), ('Magnetic', 'Magnetic'),)
    model = forms.ChoiceField(choices=CHOICES_model, required=True)
    colour = forms.ChoiceField(choices=CHOICES_colour, required=True, label=ugettext_lazy('Color'))
    additional_comments = forms.CharField(required=False, widget=forms.Textarea, label=ugettext_lazy('Additional Comments'))
    homologation = forms.BooleanField(required=False, label=ugettext_lazy('Homologation'))
    custom_clearance = forms.BooleanField(required=False, label=ugettext_lazy('Custom Clearance'))

    class Meta:
        model = models.Orders
        fields = ("model", "colour", "additional_comments")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['model'].label = ugettext_lazy('Model')
        self.fields['colour'].label = ugettext_lazy('Colour')
        self.fields['additional_comments'].label = ugettext_lazy('Additional Comments')
        self.fields['model'].widget.attrs['placeholder'] = ugettext_lazy('Modelnumber')
        self.fields['colour'].widget.attrs['placeholder'] = ugettext_lazy('What colour?')
        self.fields['additional_comments'].widget.attrs['placeholder'] = ugettext_lazy('Put extra information or remarks here')
        self.fields['homologation'].label = ugettext_lazy('Homologation: ')
        self.fields['custom_clearance'].label = ugettext_lazy('Custom Clearance: ')
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
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={
            'id': 'summernote'}))
    image = forms.ImageField()
    field_order = ['model', 'headline', 'description', 'image']

    class Meta:
        model = models.Vehicles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(VehicleForm, self).__init__(*args, **kwargs)
        self.fields['image'].label = ""
        self.fields['model'].label = ugettext_lazy("Model")
        self.fields['headline'].label = ugettext_lazy("Headline")
        self.fields['description'].label = ugettext_lazy("Description")

        self.fields['image'].widget.attrs.update({'class': 'invis'})
        self.fields['model'].widget.attrs['placeholder'] = 'Shelby Super Snake'
        self.fields['headline'].widget.attrs['placeholder'] = ugettext_lazy('Shelby Super Snake is one of the most..')
        self.fields['description'].widget.attrs['placeholder'] = ugettext_lazy('A description of the model')

class VehicleTuscanyForm(VehicleForm):
    class Meta:
        model = models.Vehicles_Tuscany
        fields = '__all__'

class NewsPostForm(forms.ModelForm):
    banner = forms.ImageField(required=False)
    title = forms.CharField(required=True)
    headline = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea(attrs={
            'id': 'summernote'}))
    quote = forms.CharField(required=False)
    quotefooter = forms.URLField(required=False)
    field_order = ['title', 'headline', 'quote', 'quotefooter', 'description', 'banner']

    class Meta:
        model = models.NewsPosts
        fields = ("title", "headline", 'quote', 'quotefooter', "description", "banner")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(NewsPostForm, self).__init__(*args, **kwargs)
        self.fields['banner'].label = ""
        self.fields['title'].label = ugettext_lazy("Title")
        self.fields['headline'].label = ugettext_lazy("Headline")
        self.fields['description'].label = ugettext_lazy("Description")
        self.fields['quote'].label = ugettext_lazy("Quote")
        self.fields['quotefooter'].label = ugettext_lazy("Quote Reference")

        self.fields['banner'].widget.attrs.update({'class': 'invis'})
        self.fields['title'].widget.attrs['placeholder'] = ugettext_lazy('Shelby Super Snake is amazing')
        self.fields['headline'].widget.attrs['placeholder'] = ugettext_lazy('Shelby Super Snake is one of the most..')
        self.fields['quote'].widget.attrs['placeholder'] = ugettext_lazy('Lorem ipsum dolor sit amet, consectetur adipiscing elit.')
        self.fields['quotefooter'].widget.attrs['placeholder'] = ugettext_lazy('From Example.com')
        self.fields['description'].widget.attrs['placeholder'] = ugettext_lazy('The actual newspost text goes here')


class NewsPostTuscanyForm(NewsPostForm):
    class Meta:
        model = models.NewsPosts_Tuscany
        fields = '__all__'

class EventForm(forms.ModelForm):
    title = forms.CharField(required=True)
    description = forms.CharField(required=True, widget=forms.Textarea)
    link = forms.URLField(required=False)
    date = forms.DateField(required=True)
    field_order = ['title', 'link', 'date', 'description']

    class Meta:
        model = models.Events
        fields = ("title", "description", "link")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = ugettext_lazy("Title")
        self.fields['description'].label = ugettext_lazy("Description")
        self.fields['date'].label = ugettext_lazy("Date")
        self.fields['link'].label = ugettext_lazy("Link")

        self.fields['title'].widget.attrs['placeholder'] = ugettext_lazy('Shelby Drag Race')
        self.fields['description'].widget.attrs['placeholder'] = ugettext_lazy('Information about the event')
        self.fields['link'].widget.attrs['placeholder'] = ugettext_lazy('http://www.example.com/event')
        self.fields['date'].widget.attrs['placeholder'] = ugettext_lazy('YYYY/MM/DD')
        self.fields['link'].help_text = ugettext_lazy("Optional. Leave blank if there is no link to the event.")

class EventTuscanyForm(EventForm):
    class Meta:
        model = models.Events_Tuscany
        fields = '__all__'

class MapDealerForm(forms.ModelForm):
    customer_name = forms.CharField(required=True)
    email = forms.EmailField(required=False)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=True)
    city = forms.CharField(required=True)
    state = forms.CharField(required=True)
    zip = forms.CharField(required=True)
    country = CountryField().formfield()
    latitude = forms.FloatField(required=True)
    longitude = forms.FloatField(required=True)
    link = forms.URLField(required=False)

    class Meta:
        model = models.MapDealers
        fields = ("customer_name", "email", "phone", "address", "city", "state", "zip", "country", "latitude", "longitude", "link")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')
        super(MapDealerForm, self).__init__(*args, **kwargs)
        self.fields['customer_name'].label = ugettext_lazy("Customer Name")
        self.fields['phone'].label = ugettext_lazy("Phone Number")
        self.fields['email'].label = ugettext_lazy("Email")
        self.fields['address'].label = ugettext_lazy("Address")
        self.fields['city'].label = ugettext_lazy("City / Town")
        self.fields['state'].label = ugettext_lazy("State / Province")
        self.fields['zip'].label = ugettext_lazy("Zip / Postal code")
        self.fields['country'].label = ugettext_lazy("Country")
        self.fields['latitude'].label = ugettext_lazy("Latitude")
        self.fields['longitude'].label = ugettext_lazy("Longitude")
        self.fields['link'].label = ugettext_lazy("Link")

        self.fields['customer_name'].widget.attrs['placeholder'] = 'American Car City'
        self.fields['phone'].widget.attrs['placeholder'] = '33169221900'
        self.fields['email'].widget.attrs['placeholder'] = 'info@americancarcity.fr'
        self.fields['address'].widget.attrs['placeholder'] = '197 BD John Kennedy'
        self.fields['city'].widget.attrs['placeholder'] = 'Corbeil-Essonnes'
        self.fields['state'].widget.attrs['placeholder'] = 'Évry'
        self.fields['zip'].widget.attrs['placeholder'] = '91100'
        self.fields['latitude'].widget.attrs['placeholder'] = '48.579013'
        self.fields['longitude'].widget.attrs['placeholder'] = '2.4766'
        self.fields['link'].widget.attrs['placeholder'] = 'https://www.company.com/about'
        self.fields['phone'].help_text = ugettext_lazy("Optional field.")
        self.fields['email'].help_text = ugettext_lazy("Optional field.")

    def save(self, commit=True):
        map = super(MapDealerForm, self).save(commit=False)

        map.customer_name = self.cleaned_data['customer_name']
        map.email = self.cleaned_data['email']
        map.phone = self.cleaned_data['phone']
        map.address = self.cleaned_data['address']
        map.country = self.cleaned_data['country']
        map.latitude = self.cleaned_data['latitude']
        map.longitude = self.cleaned_data['longitude']
        map.link = self.cleaned_data['link']

        if commit:
            map.save()

        return map



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
        self.fields['forwho'].label = ugettext_lazy("For User ID")
        self.fields['forwho'].help_text = ugettext_lazy("This field must consist of number(s) only.")

    def clean_forwho(self):
        if self.cleaned_data['forwho']:
            if Dealers.objects.filter(user=User(pk=self.cleaned_data['forwho'])).exists():
                return self.cleaned_data['forwho']
            raise forms.ValidationError('Invalid ID.')


class ContactForm(forms.Form):
    contact_name = forms.CharField(required=True, label="")
    contact_email = forms.EmailField(required=True, label="")
    contact_subject = forms.CharField(required=True, label="")
    content = forms.CharField(
        required=True,
        widget=forms.Textarea,
        label=""
    )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['contact_name'].widget.attrs.update({'class': 'input'})
        self.fields['contact_email'].widget.attrs.update({'class': 'input'})
        self.fields['contact_subject'].widget.attrs.update({'class': 'input'})
        self.fields['content'].widget.attrs.update({'class': 'input'})

        self.fields['contact_name'].widget.attrs['placeholder'] = ugettext_lazy('Name')
        self.fields['contact_email'].widget.attrs['placeholder'] = ugettext_lazy('Email')
        self.fields['contact_subject'].widget.attrs['placeholder'] = ugettext_lazy('Subject')
        self.fields['content'].widget.attrs['placeholder'] = ugettext_lazy('Message')