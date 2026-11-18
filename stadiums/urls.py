from django.urls import path
from .views import *

urlpatterns = [
    path('', home_page, name='home'),
    path("login/", login_user, name="login"),
    path("registration/", registration, name="registration"),
    path("logout/", logout_user, name="logout" ),
    path('fields/', show_fields, name='fields'),
    path('field_book/<int:id>/', book_field, name="field_book")
]
