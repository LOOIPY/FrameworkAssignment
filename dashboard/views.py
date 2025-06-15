from django.shortcuts import render
from datetime import datetime


def home(request):
    today = datetime.now().strftime("%B %d, %Y")
    return render(request, 'dashboard/home.html', {'today': today})

def checklist(request):
    return render(request, 'dashboard/checklist.html')

def invoice(request):
    return render(request, 'dashboard/invoice.html')