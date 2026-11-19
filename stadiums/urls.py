from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path("login/", login_user, name="login"),
    path("registration/", registration, name="registration"),
    path("logout/", logout_user, name="logout" ),
    path('fields/', show_fields, name='fields'),
    path('field_book/<int:id>/', book_field, name="field_book"),
    path('my_fields/', my_fields, name='my_fields'),
    path('cancel_booking/<int:id>/', cancel_booking, name="cancel_booking"),
    path('finish_booking/<int:id>/', finish_booking, name="finish_booking"),
    path("profile/", profile, name="profile"),
    path("field_info/<int:id>/", field_info, name="field_info"),
    path('bookings/<int:id>/', booking_info, name='booking_info'),
    path('play-together/', play_together, name='play_together'),
    # path('join_booking/<int:id>/', join_booking, name='join_booking'),
    # path('leave_booking/<int:id>/', leave_booking, name='leave_booking'),
]