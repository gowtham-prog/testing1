from django.shortcuts import render,HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import *
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def index(request):
    # Authenticated users view their inbox
    if request.user.is_authenticated:
        current = request.user
        list = patient.objects.filter(Creator=current).all()
        if list is not None:
            return render(request,"appointments/show.html",{
                "list": list
            })
        else:
           return render(request, "appointments/layout.html")
    # Everyone else is prompted to sign in
    else:
        return HttpResponseRedirect(reverse("login"))
@login_required(login_url='/login')  
def book (request):

    if request.method =='POST': 
        time=datetime.datetime.now()
        current=request.user
        auc= patient()
        auc.Name= request.POST["name"]
        auc.Age=request.POST["age"]
        aucGender= request.POST["gender"]
        aucHospital= request.POST["hospital"]
        aucDoctor=request.POST["doctor"]
        auc.Hospital=hospital.objects.get(id=aucHospital)
        auc.Gender = gender.objects.get(id=aucGender)
        auc.Doctor=  doctor.objects.get(id= aucDoctor)
        auc.Problem= request.POST["problem"]
        auc.Date = request.POST["date"]
        auc.timestamp = request.POST["time"]
        auc.Creator= current
        
        auc.save()
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "appointments/appointment.html",{
            "hospital":hospital.objects.all(),
            "gender": gender.objects.all(),
            "department": department.objects.all(),
            "doctor": doctor.objects.all()
        })  
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        
        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, username=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "appointments/login.html", {
                "message": "Invalid email and/or password."
            })
    else:
        return render(request, "appointments/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
   if request.method == "POST":
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        username = email
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "appointments/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user( username,email, password)
            user.first_name= firstname
            user.last_name= lastname
            user.save()
        except IntegrityError as e:
            print(e)
            return render(request, "appointments/register.html", {
                "message": "Email address already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
   else:
        return render(request, "appointments/register.html")
def home(request):
    return render(request,"appointments/layout.html")


@login_required(login_url='/login')  
def cancel(request,id):
    p = patient.objects.get(id=id)
    time=datetime.datetime.now().hour
    
    time2=p.timestamp
    time2 = str(time2)
    time2 = int(time2[0:2])

    if time2-time >1 :
        p.Active = False
        p.save()
        return HttpResponseRedirect(reverse("index"))
    
    else:

        return render(request,'appointments/show.html',{
            "message": f"Cancellation cant be done before 1 hour {time-time2}"
        })
