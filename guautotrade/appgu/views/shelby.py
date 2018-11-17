from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import send_mail
from django.http import HttpResponse
import json
from django.utils.translation import gettext as _

from .. import forms

from ..models import Vehicles, NewsPosts

# Shelby index (homepage)
def index(request):
    vehicle_list = Vehicles.objects.all()
    if len(vehicle_list) != 0:
        # the c_type determines what style class each vehicle item gets
        c_type = 0

        if len(vehicle_list) % 3 == 1:
            c_type = 1
        elif len(vehicle_list) % 3 == 2:
            c_type = 2

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

# news page
def news(request):
    if request.method == 'GET' and 'n' in request.GET:
        n = request.GET['n']
        if n is not None and n != '':
            news_list = NewsPosts.objects.filter(pk=request.GET.get('n'))
            if len(news_list) == 0:
                exists = False
            else:
                exists = True
            return render(request, 'shelby/news.html', {'newsposts': news_list, 'exists': exists, 'news': NewsPosts.objects.order_by('-date'), 'singlepost': True})
    else:
        news_list = NewsPosts.objects.order_by('-date')[:30]
        if len(news_list) == 0:
            exists = False
        else:
            exists = True
        paginator = Paginator(news_list, 1)  # Show 1 newspost per page
        page = request.GET.get('page')
        newsposts = paginator.get_page(page)
        return render(request, 'shelby/news.html', {'newsposts': newsposts, 'exists': exists, 'news': news_list})

    if not news:
        return render(request, 'shelby/news.html', {"exists": False})
    l = []
    for i in news:
        l.append(i.banner)
        l.append(i.title)
        l.append(i.headline)
        l.append(i.description)
        l.append(i.quote)
        l.append(i.quotefooter)
        l.append(i.date)

    return render(request, 'shelby/news.html',
                  {'banner': l[0], 'title': l[1], 'headline': l[2], 'desc': l[3], 'quote': l[4], 'quotefooter': l[5], 'date': l[6], 'exists': True})

# press and media page
def pressandmedia(request):
    return render(request, 'shelby/media.html')


# contact page
def contact(request):
    form_class = forms.ContactForm(auto_id=False)
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            contact_name = request.POST.get('contact_name')
            contact_email = request.POST.get('contact_email')
            contact_subject = request.POST.get('contact_subject')

            form_content = request.POST.get('content')

            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'contact_subject': contact_subject,
                'form_content': form_content
            }

            contact_message = get_template('shelby/contact_template.txt').render(context)

            send_mail("New contact form submission", contact_message, "contactmessage@guautotrade.com", ['info@guautotrade.com'], fail_silently=False)

            response_data = {'result': _("Mail has been sent. We'll respond as soon as possible!"), 'status': 'success'}
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    return render(request, 'shelby/contact.html', {'form': form_class})

# description page for a particular vehicle
def vehicledesc(request):
    form = forms.QuoteForm(auto_id=False)   
    if request.method == "GET" and 'v' in request.GET:
        v = request.GET['v']
        if v is not None and v != '':
            vehicles = Vehicles.objects.filter(pk=request.GET.get('v'))
            if not vehicles:
                return render(request, 'shelby/vehicledesc.html', {"exists": False})
            l = []
            for i in vehicles:
                l.append(i.image)
                l.append(i.model)
                l.append(i.headline)
                l.append(i.description)
                l.append(i.extra)

            return render(request, 'shelby/vehicledesc.html', {'image': l[0], 'model': l[1], 'headline': l[2], 'desc': l[3], 'extra': l[4], 'exists': True, 'vehicles': Vehicles.objects.all(), 'form': form})
    elif request.method == "POST":
        form = forms.QuoteForm(request.POST)
        if form.is_valid():
            firstname = request.POST.get('firstname')
            surname = request.POST.get('surname')
            vehicle = request.POST.get('vehicle')
            email = request.POST.get('email')
            telephone = request.POST.get('telephone')
            color = request.POST.get('color')
            comments = request.POST.get('comments')

            context = {
                'firstname': firstname,
                'surname': surname,
                'vehicle': vehicle,
                'email': email,
                'telephone': telephone,
                'color': color,
                'comments': comments
            }

            contact_message = get_template('shelby/quote_template.txt').render(context)

            send_mail("Shelby Quote & delivery request", contact_message, "quoterequests@guautotrade.com", ['info@guautotrade.com'], fail_silently=False)

            response_data = {'result': _("Request has been sent. You will be notified as soon as possible."), 'status': 'success'}
            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
        else:
            newform = forms.QuoteForm()
            response_data = {'result': _("Failed to submit."), 'status': 'failed', 'formerr': form.errors,
                                'form': str(newform)}

            return HttpResponse(
                json.dumps(response_data),
                content_type="application/json"
            )
    return render(request, 'shelby/vehicledesc.html', {'form': form})