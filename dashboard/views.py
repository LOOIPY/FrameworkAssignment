from django.shortcuts import render
from datetime import datetime

def checklist(request):
    return render(request, 'dashboard/checklist.html')

def invoice(request):
    return render(request, 'dashboard/invoice.html')