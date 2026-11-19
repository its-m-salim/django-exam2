from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import *
from django.db.models import Q



def home_page(request):
    return render(request, 'home.html')


def registration(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            return redirect("registration")

        User.objects.create_user(
            username=username,
            password=password,
            email=data.get("email"),
            avatar=request.FILES.get('avatar'),
            phone=data.get('phone'),
            bio=data.get('bio')
        )

        return redirect("login")

    return render(request, "registration.html")


def login_user(request):
    if request.method == 'POST':
        data = request.POST
        user = authenticate(
            username=data.get('username'),
            password=data.get('password')
        )

        if user is None:
            return render(request, "login.html")

        login(request, user)
        return redirect("home")

    return render(request, "login.html")




@login_required
def logout_user(request):
    logout(request)
    return redirect("login")



@login_required
def show_fields(request):

    fields = Field.objects.all().select_related("category")
    categories = Category.objects.all()

    q  = request.GET.get("q")
    category = request.GET.getlist("category")

    if q:
        fields.filter(
            Q(name__icontains = q) | Q(address__icontains = q)
        )
    if category:
        fields = fields.filter(category__id__in = category)


    context = {
        "fields": fields,
        "categories" : categories,
        "q": q,
        "q_category": category
    }

    return render(request, 'fields.html' , context)



@login_required
def book_field(request, id):

    field = get_object_or_404(Field, pk=id)

    if not field.is_available:
        return redirect("fields") 


    has_team = request.POST.get('has_team')

    if has_team not in ("True", "False"):
        return redirect("field_book", id=id)

    
    if has_team == "True":
    
        players_needed = 0

    

    if request.method == 'POST':
        data = request.POST
        Booking.objects.create(
            user = request.user,
            field = field,
            has_team = (has_team == True),
            players_needed = players_needed
        )

        field.is_available = False
        field.save()

        return redirect("home")

    return render(request, 'book_field.html', {"field": field})



@login_required
def field_info(request, id):
    field = get_object_or_404(Field, pk=id)
    return render(request, "field_info.html", {"field": field})


@login_required
def my_fields(request):
    bookings = request.user.bookings.select_related("field")

    active = bookings.filter(status = "active")
    history = bookings.exclude(status = "active")

    context = {
        "active": active,
        "history": history
    }
    return render(request, "my_fields.html", context)




@login_required
def booking_info(request, id):

    booking = get_object_or_404(Booking, pk = id, user = request.user)

    return render(request, "my_booking_info.html", {"booking": booking})



@login_required
def cancel_booking(request, id):
    booking = get_object_or_404(Booking , pk = id, user = request.user, status = "active")


    if request.method == 'POST':
        booking.status = "cancelled"
        booking.save()
        booking.field.is_available = True
        booking.field.save()

        return redirect("my_fields")

    return render(request, 'cancel_booking.html')


@login_required
def finish_booking(request, id):
    booking = get_object_or_404(Booking , pk = id, user = request.user, status = "active")


    if request.method == 'POST':
        booking.status = "completed"
        booking.save()
        booking.field.is_available = True
        booking.field.save()

        return redirect("my_fields")

    return render(request, 'cancel_booking.html')





# @login_required
# def play_together(request):

#     active_bookings = Booking.objects.filter(status = "active", has_team = False).select_related()


@login_required
def profile(request):
    return render(request, "profile.html")