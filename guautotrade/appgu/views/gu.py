from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.core.mail import send_mail
from .. import forms

def index(request):
    return render(request, 'gu/index.html')

def about(request):
    return render(request, 'gu/about.html')

def services(request):
    return render(request, 'gu/services.html')

def contact(request):
    form_class = forms.ContactForm(auto_id=False)

    if request.method == 'POST':
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

            contact_message = get_template('gu/contact_template.txt').render(context)

            send_mail("New contact form submission", contact_message, "messages@guautotrade.com", [contact_email], fail_silently=False)

            return redirect('contact')

    return render(request, 'gu/contact.html', {
        'form': form_class,
    })