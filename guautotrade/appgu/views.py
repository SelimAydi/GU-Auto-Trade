from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from django.contrib.auth.views import login

def index(request):
    return render(request, 'index.html')
	
def shelby(request):
    return render(request, 'shelby/index.html')

def contact(request):
    return render(request, 'shelby/contact.html')

def vehicledesc(request):
    return render(request, 'shelby/vehicledesc.html')

def dealerportal(request):
	errors = []
	if request.user.is_authenticated:
		if request.method == "POST":
			print("GETTING POST")
			if not request.POST.get('model') or not request.POST.get('colour'):
				if not request.POST.get('model'):
					errors.append("Model not selected.")
				elif not request.POST.get('colour'):
					errors.append("No colour was given")
				return render(request, 'dealerportal.html', {'errors' : errors})
			return render(request, 'success.html', {'model' : request.POST.get('model'), 'colour' : request.POST.get('colour')})
		else:
			print("SHOWING FORM")
			form = forms.OrderForm()
			return render(request, 'dealerportal.html', {'form' : form})
	else:
		errors.append("You need to be logged in to reach this area. Redirecting..")
		return redirect(login)