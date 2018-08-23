from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
import json


def my_view(request):
    if request == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        response_data = {}
        if user is not None:
            response_data['status'] = 'succes'
            login(request, user)
            # Redirect to a success page.
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            response_data['status'] = 'failed'
            # Return an 'invalid login' error message.
            return HttpResponse(json.dumps(response_data), content_type="application/json")

    return render(request, 'portal/index.html', {'orders': allOrders})

