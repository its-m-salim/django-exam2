from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *




@login_required
def home_page(request):
    return render(request, 'home.html')





@login_required
def logout_user(request):
    logout(request)
    return redirect("login")


def registration(request):

    if request.method == 'POST':
        data = request.POST


        if User.objects.filter(username=data['username']).exists():
            return redirect("login")

        User.objects.create_user(
            username=data['username'],
            password=data['password'],
            email = request.POST.get("email"),
            avatar = request.FILES.get('avatar'),
            phone = data['phone'],
            bio = data['bio']
        )

        return redirect("login")

    return render(request, "registration.html")




def login_user(request):

    if request.method == 'POST':
        data = request.POST
        user = authenticate(username=data['username'], password=data['password'])

        if user is None:
            return render(request, "login.html", {"error": True})

        login(request, user)
        return redirect("home")

    return render(request, "login.html")



@login_required
def show_fields(request):
    return render(request, 'fields.html' , {"fields": Field.objects.all()})



@login_required
def book_field(request, id):

    field = get_object_or_404(Field, pk=id)


    if request.method == 'POST':
        data = request.POST
        Booking.objects.create(
            user = request.user,
            field = field,
            has_team = True if data['has_team'] in ("True", "true") else False,
            players_needed = field.category.players_count if data['has_team'] in ("True", "true") else None
        )

        return redirect("home")

    return render(request, 'book_field.html')