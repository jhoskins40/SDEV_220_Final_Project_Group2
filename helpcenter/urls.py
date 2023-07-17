'''Generic module doc-string.'''
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
]
