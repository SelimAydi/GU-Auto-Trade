from django.http import HttpResponse
import json
from django.shortcuts import render, redirect
from ..models import Vehicles, Dealers, Orders, NewsPosts, Events
from .. import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import login
from django.contrib import messages
from django.utils.translation import gettext as _

# place an order in the portal
def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            form = forms.AdminOrderForm(request.POST)
            newform = forms.AdminOrderForm()
        else:
            form = forms.OrderForm(request.POST)
            newform = forms.OrderForm()
        if request.method == "POST":
            if form.is_valid():
                userid = request.user.id
                print("VALID FORM")
                userobj = Dealers.objects.get(dealerID=userid)
                order = Orders(dealerID=userobj if 'forwho' not in request.POST or request.POST['forwho'] == '' else Dealers.objects.get(dealerID=request.POST['forwho']), model=request.POST['model'], colour=request.POST['colour'], homologation=True if 'homologation' in request.POST else False, custom_clearance=True if 'custom_clearance' in request.POST else False, additional_comments=request.POST['additional_comments'])
                order.save()
                response_data = {'result': 'Create succesful', 'status': 'success'}
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
            # form = forms.NewsPostForm()
            response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                             'form': str(newform)}

            print(form.errors)
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            return render(request, 'portal/base_form.html', {'form': newform, 'headerclass': 'portal', 'title': 'Order Form', 'lead': 'Place an order for a vehicle'})
    else:
        return redirect(login)

def addnewspost(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            form = forms.NewsPostForm()
            if request.method == 'POST':
                form = forms.NewsPostForm(request.POST, request.FILES)
                if form.is_valid():
                    v = NewsPosts(writtenby=request.user, banner=form.cleaned_data['banner'], title=request.POST['title'], headline=request.POST['headline'], quote=request.POST['quote'], quotefooter=request.POST['quotefooter'], description=request.POST['description'])
                    v.save()
                    print("CREATED ID = ", v.id)
                    # return redirect('/shelby/news/?n=' + str(v.id))
                    response_data = {'result': 'Create succesful', 'status': 'success'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    newform = forms.NewsPostForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(newform)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'fileUpload': 'True', 'title': 'Add News Post', 'lead': 'Here you can add news posts to the database, to be displayed on the website.'})
    return redirect(login)

# a personal dealer orderlist
def portalmyorders(request):
    if request.user.is_authenticated:
        if not request.user.is_staff:
            userid = request.user.id
            allOrders = Orders.objects.filter(dealerID=userid).order_by('-date')
            return render(request, 'portal/myorders.html', {'orders': allOrders})
    return redirect(login)

# an orderlist that can only be seen by a staff member (or superuser)
def portalorderlist(request):
    if request.user.is_authenticated:
        form = forms.PartialOrderForm()
        if request.method == "POST":
            print(request.POST)
            print(request.FILES)

            obj = Orders.objects.get(pk=request.POST['change'])
            obj.model = request.POST['inp3']
            obj.colour = request.POST['inp4']
            obj.scheduled_completion_date = request.POST['inp8']

            obj.homologation = request.POST['check6x']
            obj.custom_clearance = request.POST['check7x']
            obj.deposit_received = request.POST['check9x']
            obj.payment_received = request.POST['check10x']

            if request.FILES:
                obj.invoice = request.FILES['invoice']

            # obj.additional_comments = form.cleaned_data['additional_comments']

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

            obj.save()

        allOrders = Orders.objects.all().order_by('-date')
        if allOrders:
            exists = True
        else:
            exists = False
        return render(request, 'portal/orderlist.html', {'orders': allOrders, 'form': form, 'exists': exists})
    return redirect(login)

# an admin page to register a dealer
def registerdealer(request):
    if request.user.is_authenticated:
        user = "Dealer"
        if request.method == "POST":
            print("Get request ", request.POST)
            form = forms.RegistrationDealerForm(request.POST)
            if form.is_valid():
                print("form is valid")
                form.save()
                return render(request, 'portal/registered.html', {'dealer_username': request.POST.get('username'), 'dealer_firstname' : request.POST.get('firstname'), 'dealer_lastname': request.POST.get('lastname'), 'usertype': user})
            else:
                print("form invalid")
                return render(request, 'portal/registerdealer.html', {'form': form})
        form = forms.RegistrationDealerForm()
        return render(request, 'portal/registerdealer.html', {'form': form, 'usertype': user})
    return redirect(login)

# a superuser page to register an admin
def registeradmin(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            user = "Admin"
            if request.method == "POST":
                print("Get request ", request.POST)
                form = forms.RegistrationAdminForm(request.POST)
                if form.is_valid():
                    print("form is valid")
                    form.save()
                    return render(request, 'portal/registered.html', {'dealer_username': request.POST.get('username'), 'dealer_firstname' : request.POST.get('firstname'), 'dealer_lastname': request.POST.get('lastname'), 'usertype': user})
                else:
                    print("form invalid")
                    return render(request, 'portal/registerdealer.html', {'form': form})
            form = forms.RegistrationAdminForm()
            return render(request, 'portal/registerdealer.html', {'form': form, 'usertype': user})
    return redirect(login)

# a staff page to add a vehicle to the database, which will be displayed on the home page
def addvehicle(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            form = forms.VehicleForm()
            if request.method == 'POST':
                form = forms.VehicleForm(request.POST, request.FILES)
                print("IS POSTING")
                print(request.POST)
                if form.is_valid():
                    print("form is valid")
                    v = Vehicles(image=form.cleaned_data['image'], model=request.POST['model'], headline=request.POST['headline'], description=request.POST['description'])
                    v.save()
                    print("CREATED ID = ", v.id)

                    response_data = {'result': 'Create succesful', 'status': 'success'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    newform = forms.VehicleForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors, 'form': str(newform)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'fileUpload': 'True', 'title': 'Add Vehicle', 'lead': 'Here you can add vehicles to the database, to be displayed on the website.'})
    return redirect(login)

# a staff page to add a newspost to the database, which will be displayed on the home page
def addnewspost(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            form = forms.NewsPostForm()
            if request.method == 'POST':
                form = forms.NewsPostForm(request.POST, request.FILES)
                if form.is_valid():
                    v = NewsPosts(writtenby=request.user, banner=form.cleaned_data['banner'], title=request.POST['title'], headline=request.POST['headline'], quote=request.POST['quote'], quotefooter=request.POST['quotefooter'], description=request.POST['description'])
                    v.save()
                    print("CREATED ID = ", v.id)
                    # return redirect('/shelby/news/?n=' + str(v.id))
                    response_data = {'result': 'Create succesful', 'status': 'success'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    newform = forms.NewsPostForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(newform)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'fileUpload': 'True', 'title': 'Add News Post', 'lead': 'Here you can add news posts to the database, to be displayed on the website.'})
    return redirect(login)

def addeventpost(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            form = forms.EventForm()
            if request.method == 'POST':
                form = forms.EventForm(request.POST)
                if form.is_valid():
                    e = Events(title=request.POST['title'], description=request.POST['description'], link=request.POST['link'], date=request.POST['date'])
                    e.save()
                    print("CREATED ID = ", e.id)
                    response_data = {'result': _("Event succesfully added."), 'status': 'success'}
                    # messages.success(request, 'Your password was updated successfully!')
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    newform = forms.EventForm()
                    response_data = {'result': _("Failed to add event."), 'status': 'failed', 'formerr': form.errors,
                                     'form': str(newform)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'title': 'Add Event', 'lead': 'Here you can add events to the database, to be displayed on the events calendar.'})
    return redirect(login)

def addmapdealer(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            form = forms.MapDealerForm()
            if request.method == 'POST':
                form = forms.MapDealerForm(request.POST)
                print("POSTING")
                if form.is_valid():
                    print("IS VALID")
                    # m = MapDealers(customer_name=request.POST['customer_name'], phone=request.POST['phone'], email=request.POST['email'], address=request.POST['address'], country=dict(countries)[request.POST['country']], latitude=request.POST['latitude'], longitude=request.POST['longitude'])
                    # m.save()
                    form.save()
                    # print("CREATED ID = ", m.id)

                    response_data = {'result': 'Create succesful', 'status': 'success'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    print("IS NOT VALID")
                    newform = forms.MapDealerForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(newform)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'title': 'Add Map Dealer', 'lead': 'Lorem Ipsum', 'extra': '<input type="hidden" id="region">'})
    return redirect(login)


def changePassword(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            print("Get request ", request.POST)
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                print("form is valid")
                form.save()
                update_session_auth_hash(request, form)
                response_data = {'result': 'Create succesful', 'status': 'success'}
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
            else:
                newform = PasswordChangeForm(request.user)
                response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                 'form': str(newform)}

                print("form invalid")
                return HttpResponse(
                    json.dumps(response_data),
                    content_type="application/json"
                )
        form = PasswordChangeForm(request.user)
        return render(request, 'portal/base_form.html', {'form': form, 'title': 'Change Password', 'lead': 'If you would like to change your password, fill out this form.'})
    return redirect(login)