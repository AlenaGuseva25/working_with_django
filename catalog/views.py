from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home_catalog(request):
    return render(request, 'catalog/home.html')

def contacts_catalog(request):
    return render(request, 'catalog/contacts.html')
