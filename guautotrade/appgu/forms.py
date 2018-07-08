from django import forms

from . import models

class OrderForm(forms.ModelForm):
	def __init__(self, *args, **kwargs):
		kwargs.setdefault('label_suffix', '')
		super(OrderForm, self).__init__(*args, **kwargs)
	class Meta:
		model = models.Orders
		fields = ['model', 'colour']
		widgets = {
			'model': forms.TextInput(attrs={'placeholder': 'The model'}),
			'colour': forms.TextInput(attrs={'placeholder': 'What colour?'}),
		}
		labels = {
            'model': 'Model',
			'colour': 'Colour',
        }