'''Generic module doc-string.'''
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home', views.redirect_home, name='redirect_home'),
    path('about', views.about, name='about'),
    path("tickets/", views.tickets, name="tickets"),
    path("tickets/create", views.create, name="create"),
    path("tickets/all", views.list, name="list"),
    path("login", views.login_user, name="login"),
    path("register_user", views.register_user, name="register_user"),
    path("logout_user", views.logout_user, name="logout"),
    path("tickets/edit/<int:ticket_id>", views.edit_ticket, name="edit_ticket"),
    path("delete_ticket/<int:ticket_id>", views.delete_ticket, name="delete-ticket"),
    path('tickets/edit/status/<int:ticket_id>/', views.edit_ticket_status, name='edit_ticket_status'),
]


handler404 = 'helpcenter.views.redirect_to_homepage'