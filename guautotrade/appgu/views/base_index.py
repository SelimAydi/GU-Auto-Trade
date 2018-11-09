from django.shortcuts import render
from ..models import Vehicles_Tuscany

def index(request):
    ftx = Vehicles_Tuscany.objects.filter(model='F150 FTX')
    blackops = Vehicles_Tuscany.objects.filter(model='F150 Black Ops')

    if ftx.exists():
        ftx = ftx[0].id
    else:
        ftx = '#'

    if blackops.exists():
        blackops = blackops[0].id
    else:
        blackops = '#'
    
    return render(request, 'index.html', {'ftx': ftx, 'blackops': blackops})
