import json
from django.shortcuts import render, redirect
from . import forms
from .models import *
from django.contrib.auth.views import login
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.core import serializers
from django.http import HttpResponse
from django_countries import countries
from django.views.generic import ListView



# Guautotrade index (homepage)
def index(request):
    return render(request, 'index.html')

# Shelby index (homepage)
def shelby(request):
    vehicle_list = Vehicles.objects.all()


    if len(vehicle_list) != 0:
        print("OUT OF RANGE")
        # the c_type determines what style class each vehicle item gets
        c_type = 0

        print("AMOUNT OF VEHICLES________: " ,len(vehicle_list))
        if len(vehicle_list) % 3 == 1:
            c_type = 1
            print("1 class")
        elif len(vehicle_list) % 3 == 2:
            c_type = 2
            print("2 class")

        last = Vehicles.objects.latest('id')
        if len(vehicle_list) > 1:
            secondlast = vehicle_list.order_by('-id')[1]
        else:
            secondlast = ''
        paginator = Paginator(vehicle_list, 9)  # Show 9 contacts per page

        page = request.GET.get('page')
        vehicles = paginator.get_page(page)
        return render(request, 'shelby/index.html', {'vehicles': vehicles, 'c_type': c_type, 'last': last, 'secondlast': secondlast, 'exists': True})
    return render(request, 'shelby/index.html', {'exists': False})


# dealers page
def dealers(request):
    return render(request, 'shelby/dealers.html')


# events page
def events(request):
    return render(request, 'shelby/events.html')

# api for events
def eventsAPI(request):
    obj = Events.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")

# api for mapdealers
def mapdealersAPI(request):
    obj = MapDealers.objects.all()
    serialized_obj = serializers.serialize("json", obj)
    print(serialized_obj)
    return HttpResponse(serialized_obj, content_type="application/json")


# shop page
def shop(request):
    return render(request, 'shelby/contact.html')


# news page
def news(request):
    if request.method == 'GET' and 'n' in request.GET:
        n = request.GET['n']
        if n is not None and n != '':
            print(request.GET)
            news = NewsPosts.objects.filter(pk=request.GET.get('n'))
    else:
        news_list = NewsPosts.objects.all()
        if len(news_list) == 0:
            exists = False
        else:
            exists = True
        paginator = Paginator(news_list, 1)  # Show 1 newspost per page
        page = request.GET.get('page')
        newsposts = paginator.get_page(page)
        return render(request, 'shelby/news.html', {'newsposts': newsposts, 'exists': exists})

    if not news:
        print("nothing in news found!")
        return render(request, 'shelby/news.html', {"exists": False})
    print("found newspost(s)")
    l = []
    for i in news:
        l.append(i.banner)
        l.append(i.title)
        l.append(i.headline)
        l.append(i.description)
        l.append(i.quote)
        l.append(i.quotefooter)
        l.append(i.date)
        l.append(i.writtenby)
        print(i.title)

    return render(request, 'shelby/news.html',
                  {'banner': l[0], 'title': l[1], 'headline': l[2], 'desc': l[3], 'quote': l[4], 'quotefooter': l[5], 'date': l[6], 'writtenby': l[7], 'exists': True})
    # else:
    #     print("canceled")
    #     return render(request, 'shelby/news.html')

# press and media page
def pressandmedia(request):
    return render(request, 'shelby/contact.html')


# contact page
def contact(request):
    return render(request, 'shelby/contact.html')

# description page for a particular vehicle
def vehicledesc(request):
    if request.method == "GET" and 'v' in request.GET:
        v = request.GET['v']
        if v is not None and v != '':
            print(request.GET)
            vehicles = Vehicles.objects.filter(pk=request.GET.get('v'))
            if not vehicles:
                print("nothing in vehicles found!")
                return render(request, 'shelby/vehicledesc.html', {"exists": False})
            else:
                print("found vehicle")
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
            return render(request, 'shelby/vehicledesc.html', {'image': l[0], 'model': l[1], 'headline': l[2], 'desc': l[3], 'exists': True})
    else:
        print("canceled")
        return render(request, 'shelby/vehicledesc.html')

# place an order in the portal
def portalorder(request):
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
            # else:
                # print("INVALID FORM")
                # return render(request, 'portal/portal.html', {'form': form})
            # return redirect('status/?m=' + request.POST.get('model') + '&c=' + request.POST.get('colour'))
        else:
            # if request.user.is_staff:
            #     form = forms.AdminOrderForm()
            # else:
            #     form = forms.OrderForm()
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
                    form = forms.NewsPostForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(form)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'fileUpload': 'True', 'title': 'Add News Post', 'lead': 'Here you can add news posts to the database, to be displayed on the website.'})
    return redirect(login)

def status(request):
    if request.method == "GET":
        model = request.GET['m']
        color = request.GET['c']
        print(color)
        return render(request, 'portal/status.html', {'model': model, 'color': color})
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
                    form = forms.VehicleForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors, 'form': str(form)}

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
                    form = forms.NewsPostForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(form)}

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
                    response_data = {'result': 'Create succesful', 'status': 'success'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    form = forms.EventForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(form)}

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
                if form.is_valid():
                    m = MapDealers(customer_name=request.POST['customer_name'], phone=request.POST['phone'], email=request.POST['email'], address=request.POST['address'], country=dict(countries)[request.POST['country']], latitude=request.POST['latitude'], longitude=request.POST['longitude'])
                    m.save()
                    print("CREATED ID = ", m.id)

                    response_data = {'result': 'Create succesful', 'status': 'success'}
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
                else:
                    form = forms.MapDealerForm()
                    response_data = {'result': 'Create unsuccesful', 'status': 'failed', 'formerr': form.errors,
                                     'form': str(form)}

                    print(form.errors)
                    return HttpResponse(
                        json.dumps(response_data),
                        content_type="application/json"
                    )
            return render(request, 'portal/base_form.html', {'form': form, 'title': 'Add Map Dealer', 'lead': ''})
    return redirect(login)
