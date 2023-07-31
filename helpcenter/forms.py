from django import forms
from .models import Ticket

class EditTicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'subject']


class EditTicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']