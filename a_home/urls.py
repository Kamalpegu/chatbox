from django.urls import path
from . import views

# Giving the app a namespace helps keep reverse lookups clean
app_name = 'a_home'

urlpatterns = [
    # This points the root of 'a_home' (http://127.0.0.1:8000/) to a home view
    path('', views.home_view, name='home'),
]
