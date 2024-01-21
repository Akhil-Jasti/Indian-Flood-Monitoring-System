from myapp import accounts as user_view
from django.contrib.auth import views as auth

from django.urls import path
from . import views
app_name="myapp"
urlpatterns = [
    path('', views.index,name="home"),
    path('flood/', views.flood_data,name="flood"),

    path('accounts/login/', user_view.Login, name ='login'),
    path('logout/', auth.LogoutView.as_view(template_name ='index2.html'), name ='logout'),
    path('accounts/register/', user_view.register, name ='register'),
]