'''Generic module doc-string.'''
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import UpdateView
from .models import Ticket
from .forms import EditTicketForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import EditTicketStatusForm

# Create your views here.

def home(request):
    '''This is our homepage!'''
    return render(request, 'helpcenter/home.html', {})

def tickets(request):
    # Check if the user is authenticated (logged in)
    if request.user.is_authenticated:
        # Get all posts by the currently logged-in user
        user_tickets = request.user.posts.all().order_by('-created_at')
    else:
        user_tickets = []  # Return an empty list if the user is not logged in

    return render(request, 'helpcenter/tickets.html', {'user_tickets': user_tickets})


@login_required
def create(request):
    if request.method == "POST":
        
        ticket_title = request.POST['title']
        subject = request.POST['subject']

        if request.user.is_authenticated:
            new_ticket = Ticket(title=ticket_title, subject=subject, author=request.user)
            new_ticket.save()
            messages.success(request, "Ticket Added Successfully")
        else:
            messages.error(request, "Login to create a ticket.")

        return redirect("home")
    else:
        return render(request, 'helpcenter/create.html', {})


def about(request):

    return render(request, 'helpcenter/about.html', {})

def list(request):

    if request.user.is_staff:
        user_tickets = Ticket.objects.all().order_by('-created_at')
    else:
        user_tickets = [] 

    return render(request, 'helpcenter/list.html', {'user_tickets': user_tickets})





def login_user(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.success(request, ("There was an Error"))
            return redirect("login")
    else:
        return render(request, 'helpcenter/login.html', {})


def register_user(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("home")
        else:
            form = UserCreationForm()
    else:
        form = UserCreationForm()
    return render(request, "helpcenter/register_user.html", {'form' :form,})

def redirect_home(request):
     return redirect('home')

def logout_user(request):
    logout(request)
    messages.success(request, ("Logged Out.."))
    return redirect("home")


@login_required
def edit_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, pk=ticket_id)

    if request.user != ticket.author:
        messages.error(request, "No Permission")
        return HttpResponseRedirect(reverse('tickets'))

    if request.method == "POST":
        form = EditTicketForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Ticket Updated")
            return HttpResponseRedirect(reverse('tickets'))
    else:
        form = EditTicketForm(instance=ticket)

    return render(request, 'helpcenter/edit_ticket.html', {'form': form, 'ticket': ticket})



@login_required
def delete_ticket(request, ticket_id):
    referer_url = request.META.get('HTTP_REFERER')
    del_ticket = Ticket.objects.get(pk=ticket_id)
    del_ticket.delete()
    messages.success(request, ("Ticket Deleted"))
    return redirect(referer_url or 'default_page_name')


def update_ticket_status(request):
    if request.method == "POST":
    
        ticket_id = request.POST.get('ticket_id')
        new_status = request.POST.get("status")

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "error"})
    
def edit_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.user.is_staff:
        if request.method == 'POST':
            form = EditTicketStatusForm(request.POST, instance=ticket)
            if form.is_valid():
                form.save()
                return redirect("list")
        else:
            form = EditTicketStatusForm(instance=ticket)

        return render(request, 'helpcenter/edit_ticket_status.html', {'form': form})
    
    return redirect("home")


def redirect_to_homepage(request, exception):
    return redirect('home')