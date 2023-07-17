'''Generic module doc-string.'''
from django.shortcuts import render

# Create your views here.

def home(request):
    '''This is our homepage!'''
    return render(request, 'home.html', {})
