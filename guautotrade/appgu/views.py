from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Orders
from .models import Dealers
from django.contrib.auth.views import login
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


def index(request):
    return render(request, 'index.html')


def shelby(request):
    return render(request, 'shelby/index.html')


def contact(request):
    return render(request, 'shelby/contact.html')


def vehicledesc(request):
    return render(request, 'shelby/vehicledesc.html')


def dealerportal(request):
    if request.user.is_authenticated:
        userid = request.user.id
        if request.method == "POST":
            print(request.POST)
            form = forms.OrderForm(data=request.POST)
            if form.is_valid():
                print("VALID FORM")
                userobj = Dealers.objects.get(dealerID=userid)
                order = Orders(dealerID=userobj, model=request.POST['model'], colour=request.POST['colour'])
                order.save()
            else:
                print("INVALID FORM")
                return render(request, 'dealerportal/dealerportal.html', {'form': valform})
            return render(request, 'dealerportal/ordered.html',
                          {'model': request.POST.get('model'), 'colour': request.POST.get('colour')})
        else:
            print("SHOWING FORM")
            form = forms.OrderForm()
            return render(request, 'dealerportal/dealerportal.html', {'form': form, 'headerclass': 'portal'})
    else:
        return redirect(login)


def orderlist(request):
    if request.user.is_authenticated:
        allOrders = Orders.objects.all()
        return render(request, 'dealerportal/orderlist.html', {'orders': allOrders})
    return redirect(login)


def registerdealer(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print("Get request ", request.POST)
            form = forms.RegistrationForm(request.POST)
            if form.is_valid():
                print("form is valid")
                form.save()
                return render(request, 'dealerportal/registered.html', {'dealer_username': request.POST.get('username'), 'dealer_firstname' : request.POST.get('firstname'), 'dealer_lastname' : request.POST.get('lastname')})
            else:
                print("form invalid")
                return render(request, 'dealerportal/registerdealer.html', {'form': form})
        form = forms.RegistrationForm()
        return render(request, 'dealerportal/registerdealer.html', {'form': form})
    return redirect(login)
