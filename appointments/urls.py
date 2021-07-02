from django.contrib import admin
from django.urls import path
from . import views

urlpatterns =[
 path("",views.index, name="index"),
 path("book",views.book, name="book"),
 path("login",views.login_view,name ="login"),
 path("register",views.register, name= "register"),
 path("logout",views.logout_view,name="logout"),
 path("home",views.home,name="home"),
 path("cancel/<int:id>",views.cancel,name="cancel"),
 
]