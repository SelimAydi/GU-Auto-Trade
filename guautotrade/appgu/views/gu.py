from django.shortcuts import render

def index(request):
    return render(request, 'gu/index.html')

def about(request):
    return render(request, 'gu/about.html')

def services(request):
    return render(request, 'gu/services.html')

def contact(request):
    return render(request, 'gu/contact.html')