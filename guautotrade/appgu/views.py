from django.shortcuts import render, redirect
from django.http import HttpResponse
from . import forms
from .models import Orders
from .models import Dealers
from .models import Vehicles
from django.contrib.auth.views import login
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from django.conf import settings
from django.core.files.storage import FileSystemStorage

def index(request):
    return render(request, 'index.html')


def shelby(request):
    return render(request, 'shelby/index.html')


def contact(request):
    return render(request, 'shelby/contact.html')


def vehicledesc(request):
    if request.method == "GET" and 'v' in request.GET:
        v = request.GET['v']
        if v is not None and v != '':
            print(request.GET)
            vehicles = Vehicles.objects.filter(pk=request.GET.get('v'))
            l = []
            for i in vehicles:
                l.append(i.image)
                l.append(i.model)
                l.append(i.headline)
                l.append(i.description)
                print(i.model)
                print(i.description)

            # headline = vehicles.headline

            print(request.GET.get('q'))
            return render(request, 'shelby/vehicledesc.html', {'image': l[0], 'model': l[1], 'headline': l[2], 'desc': l[3]})
    else:
        print("canceled")
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


def myorders(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            userid = request.user.id
            allOrders = Orders.objects.filter(dealerID=userid).order_by('-date')
            return render(request, 'dealerportal/myorders.html', {'orders': allOrders})
    return redirect(login)

def orderlist(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print(request.POST)

            obj = Orders.objects.get(pk=request.POST['change'])
            obj.model = request.POST['inp3']
            obj.colour = request.POST['inp4']
            obj.scheduled_completion_date = request.POST['inp8']

            obj.homologation = request.POST['check6x']
            obj.custom_clearance = request.POST['check7x']
            obj.deposit_received = request.POST['check9x']
            obj.payment_received = request.POST['check10x']

            if str(request.POST['check6x']) == 'True' and str(obj.homologation) == 'False':
                obj = True
            elif str(request.POST['check6x']) == 'False' and str(obj.homologation) == 'True':
                print("CHECK MAKES OBJ FALSE")
                obj = False
                print("newobj: ", obj)

            if request.POST['check7x'] == 'True' and obj.custom_clearance == 'False':
                obj = True
            elif str(request.POST['check7x']) == 'False' and str(obj.custom_clearance) == 'True':
                print("CHECK MAKES OBJ FALSE")
                obj = False
                print("newobj: ", obj)

            if request.POST['check9x'] == 'True' and obj.deposit_received == 'False':
                obj = True
            elif str(request.POST['check9x']) == 'False' and str(obj.deposit_received) == 'True':
                print("CHECK MAKES OBJ FALSE")
                obj = False
                print("newobj: ", obj)

            if request.POST['check10x'] == 'True' and obj.payment_received == 'False':
                obj = True
            elif str(request.POST['check10x']) == 'False' and str(obj.payment_received) == 'True':
                print("CHECK MAKES OBJ FALSE")
                obj = False
                print("newobj: ", obj)

            # print("homologation: ", request.POST['check6x'])
            obj.save()

        allOrders = Orders.objects.all().order_by('-date')
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


def upload(request):
    # if request.method == 'POST' and request.FILES['myfile']:
    #     myfile = request.FILES['myfile']
    #     fs = FileSystemStorage()
    #     filename = fs.save(myfile.name, myfile)
    #     uploaded_file_url = fs.url(filename)
    #     return render(request, 'dealerportal/upload.html', {
    #         'uploaded_file_url': uploaded_file_url
    #     })

    form = forms.VehicleForm()
    if request.method == 'POST':
        form = forms.VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            v = Vehicles(image=form.cleaned_data['image'], model=request.POST['model'], headline=request.POST['headline'], description=request.POST['description'])
            v.save()
            print("CREATED ID = ", v.id)
            return redirect('/shelby/vehicle/?v=' + str(v.id))
        else:
            return render(request, 'dealerportal/upload.html', {'form' : form})
    return render(request, 'dealerportal/upload.html', {'form': form})
